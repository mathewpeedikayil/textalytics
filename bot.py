from openai import APIStatusError # handle 503 Service Unavailable errors
from openai import OpenAI
import dotenv
import time
import os

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
messages = [
    {"role" : "system", "content" : """
        You are a sentiment analysis assistant,
        Analyze the sentiment of the user's messages and provide a concise summary.
    """}
]

def bot():
    stream = None
    response_content = ""

    try:
        stream = client.chat.completions.create(
            model="openai/gpt-oss-20b", # using 20b model instead of the 120b model
            messages=messages,
            temperature=0.2,
            max_tokens=250,
            stream=True
        ) 

        print("Bot: ", end="", flush=True)

        for chunk in stream:
            if not chunk.choices:
                continue
            text = chunk.choices[0].delta.content
            if text:
                time.sleep(0.1) # delay to simulate typing effect
                print(text, end="", flush=True)
                response_content += text

        messages.append({"role": "assistant", "content": response_content}) # append  bot's response to the message history
        
    except APIStatusError as e:
        print(f"API call failed: {e}")
    finally:
        if stream:
            stream.close()
        print()

def chat():
    while True:
        user_input = input("You: ")
        if not user_input.strip():
            continue # skip empty input
        elif user_input.strip().lower() == "quit":
            print("Thank you for using Textalytics!")
            break 
        elif user_input.strip().lower() == "history":
            print("Chat History: " + str(messages))
        else:
            messages.append({"role": "user", "content": user_input})
            bot()

def main():
    print("Welcome to Textalytics!")
    print("Type a sentence to perform sentiment analysis.")
    print("Type 'history' to view chat history or 'quit' to exit.")
    chat()

if __name__ == "__main__":
    main()

# References
# Build Your First AI Chatbot with Python (No OpenAI API Cost!)
# https://www.youtube.com/watch?v=WjtBdKrZzf4

# GroqCloud
# https://console.groq.com/playground?model=openai/gpt-oss-120b

# Build a Smarter AI Chatbot with Python | Memory, Streaming & Tokens
# https://www.youtube.com/watch?v=F4xn2GUVr84