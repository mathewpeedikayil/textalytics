from openai import OpenAI
import dotenv
import time
import os

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
messages = [
    {"role" : "system", "content" : """
        You are a helpful assistant,
        Give concise responses
    """}
]

def bot():
    stream = client.chat.completions.create(
        model="openai/gpt-oss-20b", # using 20b model instead of the 120b model
        messages=messages,
        temperature=0.2,
        max_tokens=150,
        stream=True
    ) 
    response_content = ""
    print("Bot: ", end="", flush=True)
    try:
        for chunk in stream:
            if not chunk.choices:
                continue
            text = chunk.choices[0].delta.content
            if text:
                time.sleep(0.1) # delay to simulate typing effect
                print(text, end="", flush=True)
                response_content += text
    finally:
        stream.close()
        print()

    messages.append({"role": "assistant", "content": response_content}) # append  bot's response to the message history

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