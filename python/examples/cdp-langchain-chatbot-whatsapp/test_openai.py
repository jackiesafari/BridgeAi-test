from dotenv import load_dotenv
import os
import openai

load_dotenv()

def test_openai_key():
    try:
        api_key = os.getenv('OPENAI_API_KEY')

        if not api_key:
            print("❌ Error: OPENAI_API_KEY is missing! Make sure it's set in your .env file.")
            return False

        print(f"✅ OpenAI Key found: {api_key[:7]}...")

        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # Test OpenAI with a simple message
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say hello!"}],
            max_tokens=2  # Keep it small to save tokens
        )

        print("✅ OpenAI API call successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True

    except openai.OpenAIError as e:
        print(f"❌ OpenAI API Error: {e}")
    except Exception as e:
        print(f"❌ General Error: {e}")

    return False

if __name__ == "__main__":
    test_openai_key()
