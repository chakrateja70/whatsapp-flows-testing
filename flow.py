"""
WhatsApp Flow Business Logic

This module handles the flow state management and screen navigation.
Customize the screens and logic based on your specific flow requirements.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


async def get_next_screen(decrypted_body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process flow request and return appropriate screen response
    
    Args:
        decrypted_body: Decrypted request body from WhatsApp
        
    Returns:
        Screen response to be encrypted and sent back
    """
    action = decrypted_body.get("action")
    screen = decrypted_body.get("screen")
    data = decrypted_body.get("data", {})
    flow_token = decrypted_body.get("flow_token")
    
    logger.info(f"Processing action: {action}, screen: {screen}")
    
    # Handle different actions
    if action == "ping":
        # Health check from WhatsApp
        return {
            "version": decrypted_body.get("version", "3.0"),
            "data": {
                "status": "active"
            }
        }
    
    elif action == "INIT":
        # Initialize flow - return first screen
        return {
            "version": decrypted_body.get("version", "3.0"),
            "screen": "WELCOME",
            "data": {
                "welcome_message": "Welcome to our service!",
                "flow_token": flow_token
            }
        }
    
    elif action == "data_exchange":
        # Handle data exchange between screens
        return handle_data_exchange(screen, data, flow_token, decrypted_body)
    
    else:
        # Unknown action
        logger.warning(f"Unknown action received: {action}")
        return {
            "version": decrypted_body.get("version", "3.0"),
            "data": {
                "error": f"Unknown action: {action}"
            }
        }


def handle_data_exchange(
    screen: str,
    data: Dict[str, Any],
    flow_token: str,
    decrypted_body: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle data exchange for different screens
    
    Args:
        screen: Current screen name
        data: Form data from the screen
        flow_token: Flow token for this session
        decrypted_body: Full decrypted request body
        
    Returns:
        Response with next screen or completion
    """
    version = decrypted_body.get("version", "3.0")
    
    # Example: Handle different screens
    if screen == "WELCOME":
        # User submitted data from welcome screen
        return {
            "version": version,
            "screen": "DETAILS",
            "data": {
                "user_name": data.get("name", "User"),
                "message": "Please provide more details"
            }
        }
    
    elif screen == "DETAILS":
        # User submitted details
        # You can save this data to database here
        user_details = {
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone")
        }
        
        logger.info(f"User details submitted for flow_token: {flow_token}")
        
        # Return success screen
        return {
            "version": version,
            "screen": "SUCCESS",
            "data": {
                "success": True,
                "message": f"Thank you, {user_details['name']}!",
                "confirmation_id": flow_token
            }
        }
    
    elif screen == "SUCCESS":
        # Flow completion
        return {
            "version": version,
            "data": {
                "extension_message_response": {
                    "params": {
                        "flow_token": flow_token,
                        "some_param_name": "some_param_value"
                    }
                }
            }
        }
    
    else:
        # Unknown screen
        logger.warning(f"Unknown screen received: {screen}")
        return {
            "version": version,
            "data": {
                "error": f"Unknown screen: {screen}"
            }
        }


# Additional helper functions for your business logic

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    import re
    # Simple validation - adjust based on your requirements
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone) is not None


async def save_flow_data(flow_token: str, data: Dict[str, Any]) -> bool:
    """
    Save flow data to database
    
    Args:
        flow_token: Unique flow token
        data: Data to save
        
    Returns:
        True if successful
    """
    # TODO: Implement database storage
    # Example:
    # await db.flows.insert_one({
    #     "flow_token": flow_token,
    #     "data": data,
    #     "created_at": datetime.utcnow()
    # })
    return True


async def get_flow_data(flow_token: str) -> Dict[str, Any]:
    """
    Retrieve flow data from database
    
    Args:
        flow_token: Unique flow token
        
    Returns:
        Flow data or empty dict
    """
    # TODO: Implement database retrieval
    # Example:
    # result = await db.flows.find_one({"flow_token": flow_token})
    # return result.get("data", {}) if result else {}
    return {}
