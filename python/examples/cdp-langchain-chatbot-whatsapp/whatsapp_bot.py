from flask import Flask, request, Response
from dotenv import load_dotenv
import os
import requests
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from cdp import Cdp  # Ensure this import is correct

# Load environment variables
load_dotenv()

# Configure CDP
api_key_name = os.getenv('CDP_API_KEY_NAME')
api_key_private_key = os.getenv('CDP_API_KEY_PRIVATE_KEY')
Cdp.configure(api_key_name, api_key_private_key)

# Configure OpenAI with GPT-4o
llm = ChatOpenAI(model="gpt-4o")

app = Flask(__name__)

# WhatsApp Configuration
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
VERSION = os.getenv('VERSION', 'v17.0')

# Store user sessions
user_sessions = {}



def get_or_create_session(phone_number):
    if phone_number not in user_sessions:
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        user_sessions[phone_number] = {
            'memory': memory
        }
    return user_sessions[phone_number]

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
        print(f"WhatsApp API Response: {response.json()}")  # Debug print
        if response.status_code != 200:
            print(f"Error sending message: {response.text}")  # Debug print
        return response.json()
    except Exception as e:
        print(f"Exception in send_whatsapp_message: {str(e)}")  # Debug print
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
        return Response(status=403)
    return Response(status=403)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received webhook data:", data)
    
    if data['object'] == 'whatsapp_business_account':
        try:
            for entry in data['entry']:
                for change in entry['changes']:
                    if 'messages' in change['value']:
                        phone_number = change['value']['messages'][0]['from']
                        message = change['value']['messages'][0]['text']['body']
                        print(f"Received message: {message} from {phone_number}")

                        session = get_or_create_session(phone_number)
                        memory = session['memory']

                        try:
                            # Use OpenAI for chat response
                            response = llm.invoke([HumanMessage(content=message)])

                            bot_reply = response.content
                            print(f"Agent response: {bot_reply}")

                            send_whatsapp_message(phone_number, bot_reply)
                        except Exception as e:
                            print(f"Error processing message: {str(e)}")
                            return 'Error', 500
            
            return 'OK', 200
        except Exception as e:
            print(f"Error in webhook: {str(e)}")
            return 'Error', 500
    
    return 'Not a WhatsApp message', 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
