from fastapi import FastAPI, Request
import requests
import asyncio
from chatbot import initialize_agent  # Import chatbot initialization

app = FastAPI()

# Initialize chatbot agent
agent_executor, config = initialize_agent()

# WhatsApp Webhook Endpoint
@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    data = await request.json()
    message = data.get("messages", [])[0].get("text", {}).get("body", "")

    # Run chatbot with WhatsApp message
    response_text = await process_chatbot_response(message)

    # Send reply back to WhatsApp
    phone_number = data.get("messages", [])[0]["from"]
    send_whatsapp_message(phone_number, response_text)

    return {"status": "ok"}

# Function to run chatbot and get response
async def process_chatbot_response(user_message):
    """Pass WhatsApp message to chatbot and return response."""
    response = []
    
    # Run agent with user message
    async for chunk in agent_executor.astream(
        {"messages": [{"role": "user", "content": user_message}]}, config
    ):
        if "agent" in chunk:
            response.append(chunk["agent"]["messages"][0].content)
        elif "tools" in chunk:
            response.append(chunk["tools"]["messages"][0].content)
    
    return " ".join(response)

# Function to send messages to WhatsApp
def send_whatsapp_message(phone, text):
    url = "https://graph.facebook.com/v19.0/YOUR_PHONE_ID/messages"
    headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": phone, "text": {"body": text}}
    requests.post(url, json=payload, headers=headers)
