from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()
client =OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

def bot(message):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": message}],
        temperature=0.2,
        max_tokens=150,
    )
    return response.choices[0].message.content

def main():
    print("Welcome to Textalytics!")
    prompt = input("Type your prompt: ")
    response = bot(prompt)
    print(response)

if __name__ == "__main__":
    main()