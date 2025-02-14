import sys
import os
from flask import Flask, request
from dotenv import load_dotenv
import requests
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from cdp import *
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


# Load environment variables before anything else
load_dotenv()

app = Flask(__name__)

# WhatsApp Configuration
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
VERSION = os.getenv('VERSION', 'v17.0')
NETWORK_ID = os.getenv('NETWORK_ID', 'base-sepolia')  # Add default network

# CDP Configuration
api_key_name = os.getenv('CDP_API_KEY_NAME')
api_key_private_key = os.getenv('CDP_API_KEY_PRIVATE_KEY')

# Debug print (masked for security)
print(f"API Key Name: {api_key_name}")
print(f"Private Key Length: {len(api_key_private_key) if api_key_private_key else 0}")
print(f"Private Key Format: {api_key_private_key[:10]}...{api_key_private_key[-10:] if api_key_private_key else ''}")

# Ensure proper PEM format
if api_key_private_key and not api_key_private_key.startswith('-----BEGIN PRIVATE KEY-----\n'):
    api_key_private_key = f"-----BEGIN PRIVATE KEY-----\n{api_key_private_key}\n-----END PRIVATE KEY-----"

try:
    # Configure CDP
    Cdp.configure(api_key_name, api_key_private_key)
    print("CDP configuration successful!")
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4")
    print("LLM initialized successfully!")
    
except Exception as e:
    print(f"Error in configuration: {str(e)}")
    sys.exit(1)

def initialize_agent():
    try:
        llm = ChatOpenAI(model="gpt-4")
        print("LLM initialized successfully!")

        agentkit = CdpAgentkitWrapper()
        cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
        tools = cdp_toolkit.get_tools()
        memory = MemorySaver()
        print("Starting Agent...")

        agent = create_react_agent(
            llm,
            tools=tools,
            checkpointer=memory,
            state_modifier=(
                "You are a helpful agent that interacts with the Polygon network using CDP Agentkit. "
                f"You can manage wallets, check balances, and make transfers on the {NETWORK_ID} network. "
                "Always verify transactions and provide clear confirmation messages. "
                "If there are any errors with private keys or permissions, explain them clearly."
            )
        )
        config = {"configurable": {"thread_id": "CDP Agentkit WhatsApp Bot!"}}
        return agent, config

    except Exception as e:
        print(f"Failed to initialize agent: {str(e)}")
        raise

# Initialize the global agent
try:
    GLOBAL_AGENT, GLOBAL_CONFIG = initialize_agent()
    print("CDP and Agent initialized successfully!")
except Exception as e:
    print(f"Error initializing CDP and Agent: {str(e)}")
    sys.exit(1)

def send_whatsapp_message(recipient, message):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {"preview_url": False, "body": message}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"WhatsApp API Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return None

@app.route('/')
def hello():
    return 'CDP WhatsApp Bot is Running!'

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge
        return 'Forbidden', 403
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
async def webhook():
    data = request.get_json()
    print("Received webhook data:", data)
    
    if data['object'] == 'whatsapp_business_account':
        try:
            for entry in data['entry']:
                for change in entry['changes']:
                    if 'statuses' in change['value']:
                        print("Received status update")
                        return 'OK', 200
                        
                    if 'messages' in change['value']:
                        phone_number = change['value']['messages'][0]['from']
                        message = change['value']['messages'][0]['text']['body']
                        print(f"Received message: {message} from {phone_number}")
                        
                        try:
                            config = {
                                "configurable": {
                                    "thread_id": phone_number,
                                    "checkpoint_ns": "whatsapp_chat",
                                    "checkpoint_id": "1"
                                }
                            }
                            
                            response = await GLOBAL_AGENT.ainvoke(
                                {"messages": [HumanMessage(content=message)]},
                                config
                            )
                            # Extract just the AI's message content
                            response_text = response['messages'][-1].content
                            print(f"Agent response: {response_text}")
                            
                            send_whatsapp_message(phone_number, response_text)
                        except Exception as e:
                            print(f"Error in processing: {str(e)}")
                            send_whatsapp_message(phone_number, "I'm having trouble processing that right now. Could you try again?")
            
            return 'OK', 200
        except Exception as e:
            print(f"Error in webhook: {str(e)}")
            return 'Error', 500
    
    return 'Not a WhatsApp message', 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)