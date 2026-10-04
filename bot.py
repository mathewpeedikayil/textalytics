import dotenv
import os

dotenv.load_dotenv()

def main():
    print("Welcome to Textalytics!")
    print(os.getenv("GROQ_API_KEY"))

if __name__ == "__main__":
    main()