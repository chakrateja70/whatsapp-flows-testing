"""
WhatsApp Cloud API Client
Send messages and manage flows using WhatsApp Business API
"""

import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class WhatsAppCloudAPI:
    """WhatsApp Cloud API Client"""
    
    def __init__(
        self,
        access_token: Optional[str] = None,
        phone_number_id: Optional[str] = None,
        api_version: str = "v21.0"
    ):
        self.access_token = access_token or os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = phone_number_id or os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.api_version = api_version or os.getenv("WHATSAPP_API_VERSION", "v21.0")
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        
        if not self.access_token:
            raise ValueError("Access token is required. Set WHATSAPP_ACCESS_TOKEN in .env")
        if not self.phone_number_id:
            raise ValueError("Phone number ID is required. Set WHATSAPP_PHONE_NUMBER_ID in .env")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """Make HTTP request to WhatsApp API"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params,
            timeout=30  # 30 seconds timeout
        )
        
        response.raise_for_status()
        return response.json()
    
    def send_text_message(self, to: str, text: str, preview_url: bool = False) -> Dict:
        """
        Send a text message
        
        Args:
            to: Recipient phone number (with country code, no +)
            text: Message text
            preview_url: Whether to show URL preview
        
        Returns:
            API response
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": text
            }
        }
        
        return self._make_request(
            "POST",
            f"{self.phone_number_id}/messages",
            data=data
        )
    
    def send_flow_message(
        self,
        to: str,
        flow_id: str,
        flow_token: str,
        header_text: str = "Start Flow",
        body_text: str = "Click the button below to start",
        footer_text: str = "",
        cta_text: str = "Open",
        screen: str = "APPOINTMENT",
        flow_action_payload: Optional[Dict] = None
    ) -> Dict:
        """
        Send a Flow message
        
        Args:
            to: Recipient phone number
            flow_id: WhatsApp Flow ID
            flow_token: Unique token for this flow instance
            header_text: Header text
            body_text: Body text
            footer_text: Footer text (optional)
            cta_text: Call-to-action button text
            screen: Initial screen to navigate to
            flow_action_payload: Additional payload data
        
        Returns:
            API response
        """
        action_payload = flow_action_payload or {"screen": screen}
        
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "flow",
                "header": {
                    "type": "text",
                    "text": header_text
                },
                "body": {
                    "text": body_text
                },
                "footer": {
                    "text": footer_text
                },
                "action": {
                    "name": "flow",
                    "parameters": {
                        "flow_message_version": "3",
                        "flow_token": flow_token,
                        "flow_id": flow_id,
                        "flow_cta": cta_text,
                        "flow_action": "navigate",
                        "flow_action_payload": action_payload
                    }
                }
            }
        }
        
        return self._make_request(
            "POST",
            f"{self.phone_number_id}/messages",
            data=data
        )
    
    def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "en_US",
        components: Optional[list] = None
    ) -> Dict:
        """
        Send a template message
        
        Args:
            to: Recipient phone number
            template_name: Template name
            language_code: Template language
            components: Template components (optional)
        
        Returns:
            API response
        """
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        if components:
            data["template"]["components"] = components
        
        return self._make_request(
            "POST",
            f"{self.phone_number_id}/messages",
            data=data
        )
    
    def mark_message_as_read(self, message_id: str) -> Dict:
        """Mark a message as read"""
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        return self._make_request(
            "POST",
            f"{self.phone_number_id}/messages",
            data=data
        )
    
    def get_media(self, media_id: str) -> Dict:
        """Get media URL"""
        return self._make_request("GET", media_id)
    
    def download_media(self, media_url: str, output_path: str):
        """Download media file"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(media_url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


class WhatsAppFlowsAPI:
    """WhatsApp Flows API Client"""
    
    def __init__(
        self,
        access_token: Optional[str] = None,
        waba_id: Optional[str] = None,
        api_version: str = "v21.0"
    ):
        self.access_token = access_token or os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.waba_id = waba_id or os.getenv("WHATSAPP_WABA_ID")
        self.api_version = api_version or os.getenv("WHATSAPP_API_VERSION", "v21.0")
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        
        if not self.access_token:
            raise ValueError("Access token is required")
        if not self.waba_id:
            raise ValueError("WABA ID is required")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> Dict:
        """Make HTTP request to WhatsApp API"""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        if files:
            response = requests.request(method=method, url=url, headers=headers, data=data, files=files, timeout=30)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.request(method=method, url=url, headers=headers, json=data, timeout=30)
        
        response.raise_for_status()
        return response.json()
    
    def create_flow(
        self,
        name: str,
        categories: list = None,
        endpoint_uri: Optional[str] = None
    ) -> Dict:
        """
        Create a new Flow
        
        Args:
            name: Flow name
            categories: Flow categories (default: ["OTHER"])
            endpoint_uri: Endpoint URI (optional)
        
        Returns:
            Flow creation response with flow ID
        """
        data = {
            "name": name,
            "categories": categories or ["OTHER"]
        }
        
        if endpoint_uri:
            data["endpoint_uri"] = endpoint_uri
        
        return self._make_request("POST", f"{self.waba_id}/flows", data=data)
    
    def get_flow(self, flow_id: str, fields: Optional[str] = None) -> Dict:
        """Get Flow details"""
        params = {"fields": fields} if fields else None
        return self._make_request("GET", flow_id, data=params)
    
    def update_flow(self, flow_id: str, **kwargs) -> Dict:
        """Update Flow metadata"""
        return self._make_request("POST", flow_id, data=kwargs)
    
    def delete_flow(self, flow_id: str) -> Dict:
        """Delete a Flow"""
        return self._make_request("DELETE", flow_id)
    
    def publish_flow(self, flow_id: str) -> Dict:
        """Publish a Flow"""
        return self._make_request("POST", f"{flow_id}/publish")
    
    def upload_flow_json(self, flow_id: str, flow_json_path: str) -> Dict:
        """
        Upload Flow JSON configuration
        
        Args:
            flow_id: Flow ID
            flow_json_path: Path to flow.json file
        
        Returns:
            Upload response
        """
        with open(flow_json_path, 'rb') as f:
            files = {'file': ('flow.json', f, 'application/json')}
            return self._make_request("POST", f"{flow_id}/assets", files=files)
    
    def deprecate_flow(self, flow_id: str) -> Dict:
        """Deprecate a Flow"""
        return self._make_request("POST", f"{flow_id}/deprecate")
    
    def get_flow_assets(self, flow_id: str) -> Dict:
        """Get Flow assets"""
        return self._make_request("GET", f"{flow_id}/assets")


# Example usage
if __name__ == "__main__":
    # Initialize API client
    api = WhatsAppCloudAPI()
    flows_api = WhatsAppFlowsAPI()
    
    # Example: Send text message
    # response = api.send_text_message(
    #     to="1234567890",
    #     text="Hello from Python!"
    # )
    # print("Text message sent:", response)
    
    # Example: Send Flow message
    # flow_id = os.getenv("WHATSAPP_FLOW_ID")
    # response = api.send_flow_message(
    #     to="1234567890",
    #     flow_id=flow_id,
    #     flow_token="unique_token_123",
    #     header_text="Book an Appointment",
    #     body_text="Schedule your appointment now",
    #     cta_text="Get Started",
    #     screen="APPOINTMENT"
    # )
    # print("Flow message sent:", response)
    
    print("✅ WhatsApp Cloud API client ready!")
    print("Uncomment examples above to send messages")
