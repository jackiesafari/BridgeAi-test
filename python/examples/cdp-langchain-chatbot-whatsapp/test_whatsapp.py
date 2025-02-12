from dotenv import load_dotenv
import os
import requests

load_dotenv()

def test_whatsapp_token():
    try:
        access_token = os.getenv('ACCESS_TOKEN')
        phone_number_id = os.getenv('PHONE_NUMBER_ID')
        version = os.getenv('VERSION', 'v17.0')
        
        print(f"WhatsApp Access Token found: {access_token[:10]}...")
        print(f"Phone Number ID found: {phone_number_id}")
        print(f"API Version: {version}")
        
        # Test WhatsApp API
        url = f"https://graph.facebook.com/{version}/{phone_number_id}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("WhatsApp API call successful!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"WhatsApp API Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"WhatsApp Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_whatsapp_token()