"""
WhatsApp Flows FastAPI Server
"""

import os
import hmac
import hashlib
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from dotenv import load_dotenv
from encryption import decrypt_request, encrypt_response, FlowEndpointException
from flow import get_next_screen

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp Flows Endpoint")

APP_SECRET = os.getenv("APP_SECRET")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PASSPHRASE = os.getenv("PASSPHRASE", "")
PORT = int(os.getenv("PORT", "3000"))


def is_request_signature_valid(signature_header: str, raw_body: bytes) -> bool:
    """Validate request signature using HMAC SHA256"""
    if not APP_SECRET:
        logger.critical("CRITICAL: App Secret is not set. Rejecting request for security.")
        logger.warning("Set APP_SECRET in .env file to accept requests.")
        return False
    
    if not signature_header:
        return False
    
    signature = signature_header.replace("sha256=", "")
    
    # Calculate expected signature
    hmac_obj = hmac.new(
        APP_SECRET.encode('utf-8'),
        raw_body,
        hashlib.sha256
    )
    expected_signature = hmac_obj.hexdigest()
    
    # Constant time comparison
    if not hmac.compare_digest(expected_signature, signature):
        logger.error("Request Signature did not match")
        return False
    
    return True


@app.post("/")
async def handle_flow_request(request: Request):
    """Main endpoint for WhatsApp Flows"""
    
    if not PRIVATE_KEY:
        raise HTTPException(
            status_code=500,
            detail='Private key is empty. Please check your env variable "PRIVATE_KEY".'
        )
    
    # Get raw body and signature
    raw_body = await request.body()
    signature_header = request.headers.get("x-hub-signature-256")
    
    # Validate signature
    if not is_request_signature_valid(signature_header, raw_body):
        return Response(status_code=432)
    
    # Parse JSON body
    body = await request.json()
    
    # Decrypt request
    try:
        decrypted_request = decrypt_request(body, PRIVATE_KEY, PASSPHRASE)
    except FlowEndpointException as e:
        logger.error(f"FlowEndpointException: {e}")
        return Response(status_code=e.status_code)
    except Exception as e:
        logger.error(f"Error decrypting request: {e}")
        return Response(status_code=500)
    
    aes_key = decrypted_request["aes_key"]
    initial_vector = decrypted_request["initial_vector"]
    decrypted_body = decrypted_request["decrypted_body"]
    
    logger.info(f"Decrypted Request - Action: {decrypted_body.get('action')}, Screen: {decrypted_body.get('screen')}")
    logger.debug(f"Full decrypted body: {decrypted_body}")
    
    # Optional: Validate flow token
    # if not is_valid_flow_token(decrypted_body.get("flow_token")):
    #     error_response = {"error_msg": "The message is no longer available"}
    #     encrypted_response = encrypt_response(error_response, aes_key, initial_vector)
    #     return Response(content=encrypted_response, status_code=427)
    
    # Get screen response
    screen_response = await get_next_screen(decrypted_body)
    logger.info(f"Screen response prepared for action: {decrypted_body.get('action')}")
    logger.debug(f"Response to encrypt: {screen_response}")
    
    # Encrypt and return response
    encrypted_response = encrypt_response(screen_response, aes_key, initial_vector)
    return Response(content=encrypted_response)


@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Webhook verification endpoint for WhatsApp
    Facebook/WhatsApp will send a GET request to verify your webhook
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    verify_token = os.getenv("WEBHOOK_VERIFY_TOKEN", "my_verify_token")
    
    if mode == "subscribe" and token == verify_token:
        logger.info("Webhook verified successfully")
        return Response(content=challenge, media_type="text/plain")
    else:
        logger.warning("Webhook verification failed")
        return Response(status_code=403)


@app.post("/webhook")
async def handle_webhook(request: Request):
    """
    Webhook endpoint for receiving WhatsApp messages and events
    This is different from the Flow endpoint (/)
    """
    body = await request.json()
    logger.info(f"Webhook received: {body}")
    
    # Process webhook events (messages, status updates, etc.)
    # Extract message data from webhook
    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if messages:
            for message in messages:
                logger.info(f"New message from {message.get('from')}: {message.get('text', {}).get('body', 'N/A')}")
                # TODO: Process incoming messages
                # You can use whatsapp_api.py to reply
        
        # Acknowledge receipt
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint"""
    return """<pre>Nothing to see here.
WhatsApp Flows Endpoint Server is running.</pre>"""


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "whatsapp-flows-endpoint"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
