from openai import APIStatusError, OpenAI
import dotenv
import os
import streamlit as st


dotenv.load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_PROMPT = """
You are Textalytics, a sentiment analysis assistant.

For each user message, analyse the text and respond with these sections:

Sentiment: one of [positive, neutral, negative, mixed]
Tone: 2-4 concise tone labels
Summary: 1 concise sentence
Evidence:
- 2-3 short quotes from the user's text that justify the sentiment/tone
Confidence: low, medium, or high

Rules:
- Base conclusions only on the user's text.
- Do not infer personal traits, mental health state, or intent beyond what is written.
- If sentiment is unclear, use "mixed" or "neutral" and explain briefly.
- Be concise and practical.
""".strip()


def initialize_messages() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def reset_messages() -> None:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def stream_assistant_response():
    stream = None
    response_content = ""

    try:
        stream = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages,
            temperature=0.2,
            max_tokens=380,
            stream=True,
        )

        for chunk in stream:
            if not chunk.choices:
                continue

            text = chunk.choices[0].delta.content
            if text:
                response_content += text
                yield text

        if response_content:
            st.session_state.messages.append(
                {"role": "assistant", "content": response_content}
            )

    except APIStatusError as error:
        yield f"\n\nAPI call failed (HTTP {error.status_code}). Please try again."
    finally:
        if stream is not None:
            stream.close()


def main() -> None:
    st.set_page_config(page_title="Textalytics", page_icon="💬", layout="wide")

    initialize_messages()
    info_col, chat_col = st.columns([1, 3], gap="large")

    with info_col:
        st.title("Textalytics")
        st.caption("Sentiment Analysis Chatbot")
        if st.button("Clear Chat", use_container_width=True):
            reset_messages()
            st.rerun()

    with chat_col:
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input("Type your sentence for sentiment analysis...")
        if not user_input:
            return

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            st.write_stream(stream_assistant_response)


if __name__ == "__main__":
    main()
