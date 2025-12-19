"""
Example usage of WhatsApp API
Demonstrates how to send different types of messages
"""

import os
from dotenv import load_dotenv
from whatsapp_api import WhatsAppCloudAPI, WhatsAppFlowsAPI

load_dotenv()


def example_send_text_message():
    """Example: Send a simple text message"""
    api = WhatsAppCloudAPI()
    
    recipient = "1234567890"  # Replace with actual number (without +)
    message = "Hello! This is a test message from your chatbot."
    
    response = api.send_text_message(recipient, message)
    print(f"Text message sent: {response}")


def example_send_text_with_url_preview():
    """Example: Send text message with URL preview"""
    api = WhatsAppCloudAPI()
    
    recipient = "1234567890"
    message = "Check out our website: https://example.com"
    
    response = api.send_text_message(recipient, message, preview_url=True)
    print(f"Message with URL preview sent: {response}")


def example_send_flow_message():
    """Example: Send a Flow message to start interactive flow"""
    api = WhatsAppCloudAPI()
    
    recipient = "1234567890"
    flow_id = os.getenv("WHATSAPP_FLOW_ID")
    flow_token = f"flow_token_{recipient}_12345"  # Unique token per user/session
    
    response = api.send_flow_message(
        to=recipient,
        flow_id=flow_id,
        flow_token=flow_token,
        header_text="📋 Registration Form",
        body_text="Please fill out this quick form to get started",
        footer_text="Takes less than 2 minutes",
        cta_text="Start",
        screen="WELCOME",
        flow_action_payload={"initial_data": "value"}
    )
    print(f"Flow message sent: {response}")


def example_send_template_message():
    """Example: Send a template message"""
    api = WhatsAppCloudAPI()
    
    recipient = "1234567890"
    template_name = "hello_world"  # Replace with your template name
    
    response = api.send_template_message(
        to=recipient,
        template_name=template_name,
        language_code="en_US"
    )
    print(f"Template message sent: {response}")


def example_send_template_with_parameters():
    """Example: Send template with dynamic parameters"""
    api = WhatsAppCloudAPI()
    
    recipient = "1234567890"
    
    # Template with parameters
    components = [
        {
            "type": "body",
            "parameters": [
                {"type": "text", "text": "John Doe"},
                {"type": "text", "text": "December 25, 2025"}
            ]
        }
    ]
    
    response = api.send_template_message(
        to=recipient,
        template_name="appointment_reminder",
        language_code="en_US",
        components=components
    )
    print(f"Template with parameters sent: {response}")


def example_create_flow():
    """Example: Create a new Flow"""
    flows_api = WhatsAppFlowsAPI()
    
    response = flows_api.create_flow(
        name="Customer Registration Flow",
        categories=["SIGN_UP"],
        endpoint_uri="https://your-server.com/"  # Your Flow endpoint
    )
    
    flow_id = response.get("id")
    print(f"Flow created with ID: {flow_id}")
    return flow_id


def example_upload_flow_json():
    """Example: Upload Flow JSON configuration"""
    flows_api = WhatsAppFlowsAPI()
    
    flow_id = "YOUR_FLOW_ID"  # Replace with actual Flow ID
    flow_json_path = "flow.json"  # Path to your flow.json file
    
    response = flows_api.upload_flow_json(flow_id, flow_json_path)
    print(f"Flow JSON uploaded: {response}")


def example_publish_flow():
    """Example: Publish a Flow"""
    flows_api = WhatsAppFlowsAPI()
    
    flow_id = "YOUR_FLOW_ID"
    
    response = flows_api.publish_flow(flow_id)
    print(f"Flow published: {response}")


def example_get_flow_details():
    """Example: Get Flow details"""
    flows_api = WhatsAppFlowsAPI()
    
    flow_id = "YOUR_FLOW_ID"
    
    response = flows_api.get_flow(
        flow_id,
        fields="name,status,categories,validation_errors"
    )
    print(f"Flow details: {response}")


def example_complete_flow_setup():
    """Example: Complete flow setup from scratch"""
    flows_api = WhatsAppFlowsAPI()
    
    # Step 1: Create Flow
    print("Creating flow...")
    create_response = flows_api.create_flow(
        name="Demo Registration Flow",
        categories=["OTHER"],
        endpoint_uri="https://your-server.com/"
    )
    flow_id = create_response.get("id")
    print(f"✓ Flow created: {flow_id}")
    
    # Step 2: Upload Flow JSON
    print("Uploading flow configuration...")
    upload_response = flows_api.upload_flow_json(flow_id, "flow.json")
    print(f"✓ Configuration uploaded")
    
    # Step 3: Publish Flow
    print("Publishing flow...")
    publish_response = flows_api.publish_flow(flow_id)
    print(f"✓ Flow published")
    
    # Step 4: Get and verify
    flow_details = flows_api.get_flow(flow_id, fields="name,status,validation_errors")
    print(f"✓ Flow status: {flow_details.get('status')}")
    
    return flow_id


def example_mark_message_as_read():
    """Example: Mark a message as read"""
    api = WhatsAppCloudAPI()
    
    message_id = "wamid.XXXXX"  # Message ID from webhook
    
    response = api.mark_message_as_read(message_id)
    print(f"Message marked as read: {response}")


if __name__ == "__main__":
    print("WhatsApp API Examples")
    print("=" * 50)
    print("\nUncomment the examples you want to run\n")
    
    # Uncomment to test:
    # example_send_text_message()
    # example_send_flow_message()
    # example_create_flow()
    # example_complete_flow_setup()
    
    print("\n✅ Examples ready to use!")
    print("Update recipient numbers and Flow IDs before running")
