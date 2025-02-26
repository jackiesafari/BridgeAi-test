from flask import Flask, request
import json
import os
import sys
import time
import requests
import random
from dotenv import load_dotenv

# LangChain and OpenAI imports
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# CDP imports
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from cdp_langchain.tools import CdpTool

# Import CoinGecko plugin
from coingecko_plugin import coingecko

# Load environment variables
load_dotenv()

# WhatsApp Configuration
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
VERSION = os.getenv('VERSION', 'v17.0')
NETWORK_ID = os.getenv('NETWORK_ID', 'polygon-mainnet')  # Default to polygon-mainnet

# CDP Configuration
api_key_name = os.getenv('CDP_API_KEY_NAME')
api_key_private_key = os.getenv('CDP_API_KEY_PRIVATE_KEY')

# Configure wallet data file path
wallet_data_file = "wallet_data.txt"

# Initialize Flask app
app = Flask(__name__)

# Load character profile
with open('character.json', 'r') as f:
    CHARACTER = json.load(f)

def get_random_style(style_type):
    """Get random style elements from character profile"""
    if style_type in CHARACTER['style']:
        return random.choice(CHARACTER['style'][style_type])
    return None

def send_whatsapp_message(to: str, message: str):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Message sent successfully: {response.json()}")
    except Exception as e:
        print(f"Failed to send message: {str(e)}")

# Initialize the global agent
GLOBAL_AGENT = None

def initialize_agent():
    try:
        llm = ChatOpenAI(model="gpt-4")
        print("LLM initialized successfully!")

        # Initialize CDP tools
        agentkit = CdpAgentkitWrapper()
        cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
        cdp_tools = cdp_toolkit.get_tools()
        
        # Initialize CoinGecko tools
        crypto_tools = coingecko().get_tools()
        print("CoinGecko tools initialized:", [tool.name for tool in crypto_tools])
        
        # Combine all tools
        all_tools = cdp_tools + crypto_tools

        # Create personality description from character.json
        bio_points = "\n".join([f"- {point}" for point in CHARACTER['bio']])
        style_points = "\n".join([f"- {point}" for point in CHARACTER['style']['all']])
        topics = ", ".join(CHARACTER['topics'])
        
        agent = create_react_agent(
            llm,
            tools=all_tools,
            state_modifier=(
                f"You are {CHARACTER['name']}, {CHARACTER['system']}\n\n"
                
                "About you:\n"
                f"{bio_points}\n\n"
                
                "Your communication style:\n"
                f"{style_points}\n\n"
                
                f"You are knowledgeable about: {topics}\n\n"
                
                "Additional capabilities:\n"
                "- You can interact with the Polygon network and provide blockchain functionality\n"
                "- You can fetch cryptocurrency prices and trending coins\n"
                "- You maintain your character's personality while providing accurate information\n\n"
                
                "Remember:\n"
                "1. Stay true to your character's personality\n"
                "2. Use the provided tools for accurate crypto data\n"
                "3. Maintain your unique style while being helpful\n"
                "4. Include Polygon network capabilities in your responses when relevant\n"
            )
        )
        return agent

    except Exception as e:
        print(f"Failed to initialize agent: {str(e)}")
        raise

# Initialize the agent
GLOBAL_AGENT = initialize_agent()

@app.route('/')
def home():
    return 'WhatsApp Bot is running!'

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge
        return 'Invalid verification token', 403
    return 'Invalid request', 400

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if data['object'] == 'whatsapp_business_account':
        try:
            for entry in data['entry']:
                for change in entry['changes']:
                    if 'messages' in change['value']:
                        message_data = change['value']['messages'][0]
                        phone_number = message_data['from']
                        message = message_data['text']['body'].lower()
                        print(f"Processing message: {message} from {phone_number}")
                        
                        # For crypto queries, add character's style
                        if 'trending' in message or 'trend' in message:
                            crypto_tools = coingecko().get_tools()
                            for tool in crypto_tools:
                                if tool.name == "get_trending_coins":
                                    base_response = tool.func()
                                    style_comment = get_random_style('chat')
                                    response_text = f"{base_response}\n\n{style_comment}"
                                    send_whatsapp_message(phone_number, response_text)
                                    return 'OK', 200
                        
                        # For all other queries, use the agent with character's personality
                        config = {
                            "configurable": {
                                "thread_id": phone_number,
                                "checkpoint_ns": "whatsapp_chat",
                                "checkpoint_id": "1"
                            }
                        }
                        
                        response = GLOBAL_AGENT.invoke(
                            {"messages": [HumanMessage(content=message)]},
                            config
                        )
                        response_text = response['messages'][-1].content
                        send_whatsapp_message(phone_number, response_text)
            
            return 'OK', 200
        except Exception as e:
            print(f"Error in webhook: {str(e)}")
            return 'Error', 500
    
    return 'Not a WhatsApp message', 404

if __name__ == '__main__':
    app.run(debug=True)