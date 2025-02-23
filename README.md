# CDP WhatsApp AI Agent

A WhatsApp agent powered by CDP (Coinbase Developer Platform) Agentkit and LangChain, enabling intelligent conversations and blockchain interactions through WhatsApp.

## Features

- WhatsApp message handling via webhooks
- AI-powered responses using GPT-4
- Blockchain interaction capabilities on Polygon network
- Autonomous and interactive chat modes
- Secure key management and environment configuration

## Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- [CDP API Key](https://portal.cdp.coinbase.com/access/api)
- [OpenAI API Key](https://platform.openai.com/docs/quickstart)
- WhatsApp Business API credentials:
  - Access Token
  - App ID
  - Phone Number ID
  - Verify Token (for webhook setup)

## Setup

1. **Clone the repository and install dependencies:**
```bash
poetry install
```

2. **Configure environment variables:**
Create a `.env` file in the project root with the following:
```
CDP_API_KEY_NAME=your_key_name
CDP_API_KEY_PRIVATE_KEY=your_private_key
OPENAI_API_KEY=your_openai_key
NETWORK_ID=polygon-mainnet
ACCESS_TOKEN=your_whatsapp_token
APP_ID=your_app_id
PHONE_NUMBER_ID=your_phone_number_id
VERIFY_TOKEN=your_verify_token
VERSION=v17.0
```

3. **Set up webhook endpoint:**
- Install and configure [ngrok](https://ngrok.com/) for local development
- Start ngrok to expose your local server:
```bash
ngrok http 5000
```
- Use the ngrok URL in the Meta Developer Portal for webhook configuration

## Running the Bot

1. **Start the WhatsApp bot:**
```bash
python whatsapp_bot.py
```

2. **Run in chat mode (for testing):**
```bash
make run
```

## Testing

Run the test suite to verify API configurations:
```bash
python -m pytest
```

Individual tests can be run for specific components:
- `test_whatsapp.py`: WhatsApp API connection
- `test_openai.py`: OpenAI API integration
- `test_cdp.py`: CDP configuration

## Troubleshooting

- Ensure all environment variables are properly set
- Verify webhook URL is correctly configured in Meta Developer Portal
- Check ngrok tunnel is active and webhook URL is up to date
- Confirm Python version compatibility (3.10+)

## License

This project is licensed under the MIT License - see the LICENSE file for details.