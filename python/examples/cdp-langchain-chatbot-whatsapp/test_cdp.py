from dotenv import load_dotenv
import os
from cdp import *

load_dotenv()

def test_cdp_key():
    try:
        # Get keys from .env file
        api_key_name = os.getenv('CDP_API_KEY_NAME')
        api_key_private_key = os.getenv('CDP_API_KEY_PRIVATE_KEY')
        
        print(f"CDP Key Name found: {api_key_name}")
        print(f"CDP Private Key starts with: {api_key_private_key[:30]}...")
        
        # Configure CDP with your keys
        Cdp.configure(api_key_name, api_key_private_key)
        print("CDP configuration successful!")
        return True
    except Exception as e:
        print(f"CDP Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_cdp_key()