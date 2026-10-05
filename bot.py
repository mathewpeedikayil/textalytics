from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

def bot(message):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": message}],
        temperature=0.2,
        max_tokens=150,
    )
    print("Bot response: ", response.choices[0].message.content)
    return response.choices[0].message.content

def chat():
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "quit":
            break
        bot(user_input)

def main():
    print("Welcome to Textalytics!")
    chat()

if __name__ == "__main__":
    main()

# References
# Build Your First AI Chatbot with Python (No OpenAI API Cost!)
# https://www.youtube.com/watch?v=WjtBdKrZzf4&t=1718s