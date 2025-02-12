# CDP Agentkit LangChain Extension Examples - WhatsApp Chatbot Python

This example demonstrates an agent setup as a Update WhatsApp """terminal""" style chatbot with access to the full set of CDP Agentkit actions.

## Ask the chatbot to engage in the Web3 ecosystem!
- "Transfer a portion of your ETH to john2879.base.eth"
- "Deploy an NFT that will go super viral!"
- "Choose a name for yourself and register a Basename for your wallet"
- "Deploy an ERC-20 token with total supply 1 billion"

## Requirements
- Python 3.10+
- Poetry for package management and tooling
  - [Poetry Installation Instructions](https://python-poetry.org/docs/#installation)
- [CDP API Key](https://portal.cdp.coinbase.com/access/api)
- [OpenAI API Key](https://platform.openai.com/docs/quickstart#create-and-export-an-api-key)


### Checking Python Version
Before using the example, ensure that you have the correct version of Python installed. The example requires Python 3.10 or higher. You can check your Python version by running the following code:

```bash
python --version
poetry --version
```

## Setup Virtual Environment

```bash
python -m venv venv
```

## Create a requirements.txt file yet and add the following dependencies:
langchain
python-dotenv
pydantic

## Installation
```bash
poetry install
```
Installation

Install the library

```bash
%pip install -qU cdp-langchain
```



## Run the Chatbot

### Set ENV Vars
- Ensure the following ENV Vars are set:
  - "CDP_API_KEY_NAME"
  - "CDP_API_KEY_PRIVATE_KEY"
  - "OPENAI_API_KEY"
  - "NETWORK_ID" (Defaults to `base-sepolia`)
  
  FOR WHATSAPP 
  - "ACCESS_TOKEN"
  - "APP_ID"
  - "RECEPIENT_WAID"
  - "VERSION"
  - "PHONE_NUMBER_ID"




```bash
make run
```

## Troubleshooting
If you encounter issues with Poetry make sure to add a PATH to your shell configuration file. 

### To get the WhatsApp API working
- Make sure to set the correct values in the .env file
- Make sure to set the correct values in the webhook.py file
 1. First, install Flask and required packages
 # Using poetry
poetry add flask python-dotenv requests
2. Create Ngrok account and install the ngrok CLI 
3. Run ngrok and get the ngrok URL
- Make sure to set the correct values in the whatsapp_bot.py file

