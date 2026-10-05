from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
messages = [
    {"role" : "system", "content" : """
        You are a helpful assistant,
        Your name is textalyticsBot,
        Give concise responses,
        Introduce yourself in the first response
    """}
]

def bot():
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.2,
        max_tokens=150,
    ) 
    response_content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_content}) # append  bot's response to the message history
    return response_content

def chat():
    while True:
        user_input = input("You: ")
        messages.append({"role": "user", "content": user_input})
        if user_input.strip().lower() == "quit":
            break 
        print(bot())

def main():
    print("Welcome to Textalytics!")
    chat()

if __name__ == "__main__":
    main()

# References
# Build Your First AI Chatbot with Python (No OpenAI API Cost!)
# https://www.youtube.com/watch?v=WjtBdKrZzf4&t=1718s

# GroqCloud
# https://console.groq.com/playground?model=openai/gpt-oss-120b