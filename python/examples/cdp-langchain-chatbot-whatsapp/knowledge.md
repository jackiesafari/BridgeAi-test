# CDP LangChain WhatsApp Chatbot

## Project Overview
WhatsApp chatbot implementation using CDP (Conversational Data Platform) and LangChain. Integrates with WhatsApp's API to provide an AI-powered chat interface.

## Key Components
- WhatsApp webhook integration for message handling
- CDP agent for conversational AI
- LangChain for language model interactions
- Autonomous and chat modes available

## Development Guidelines
- Run tests before committing changes: `python -m pytest`
- Keep API keys and tokens secure using environment variables
- Maintain test coverage for API integrations (CDP, OpenAI, WhatsApp)

## Important Links
- WhatsApp Business API Documentation: https://developers.facebook.com/docs/whatsapp/cloud-api
- CDP Documentation: https://docs.agentkit.ai/
- LangChain Documentation: https://python.langchain.com/docs/get_started/introduction

## Project Structure
- `whatsapp_bot.py`: Core WhatsApp integration and message handling
- `chatbot.py`: CDP agent initialization and chat modes
- Test files for each integration component

## Configuration
Uses Poetry for dependency management. Required environment variables:
- WhatsApp API token
- CDP API key
- OpenAI API key
