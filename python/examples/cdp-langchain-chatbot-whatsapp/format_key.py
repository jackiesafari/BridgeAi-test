from dotenv import load_dotenv
import os
from cdp import *

load_dotenv()

# Get the key
api_key_name = os.getenv('CDP_API_KEY_NAME')
api_key_private_key = os.getenv('CDP_API_KEY_PRIVATE_KEY')

print("Key name:", api_key_name)
print("Private key format:")
print(api_key_private_key)

try:
    # Try to configure CDP
    Cdp.configure(api_key_name, api_key_private_key)
    print("CDP configuration successful!")
except Exception as e:
    print("Error:", str(e))