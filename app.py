import csv
from openai import APIStatusError, OpenAI
import dotenv
import os
from pathlib import Path
import random
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
Evidence: 2-3 short quotes from the user's text that justify the sentiment/tone
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


@st.cache_data
def load_combined_rows(csv_path: str = "data/combined.csv"):
    path = Path(csv_path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def get_dataset_label(sample: dict) -> str:
    label_text = str(sample.get("label", "")).strip()
    if label_text == "1":
        return "positive"
    if label_text == "0":
        return "negative"
    return label_text if label_text else "Not available"


def get_latest_message_content(role: str) -> str:
    for message in reversed(st.session_state.messages):
        if message.get("role") == role:
            return message.get("content", "")
    return ""


def main() -> None:
    st.set_page_config(page_title="Textalytics", page_icon="💬", layout="wide")

    initialize_messages()
    rows = load_combined_rows("data/combined.csv")
    if rows and "random_sample" not in st.session_state:
        first_sample = random.choice(rows)
        st.session_state.random_sample = first_sample
        first_sentence = first_sample.get("sentence") or first_sample.get("text") or ""
        if first_sentence:
            st.session_state.pending_user_input = first_sentence

    sample = st.session_state.get("random_sample")
    dataset_label = get_dataset_label(sample) if sample else "Not available"
    _, main_col, _ = st.columns([0.5, 3, 0.5])
    with main_col:
        if not rows:
            st.info("No data found. Add data/combined.csv to the project.")
            return

        st.title("Textalytics")
        st.caption("Sentiment Analysis Bot")

        left_col, right_col = st.columns(2, gap="small")
        progress_placeholder = None
        with left_col:
            with st.container(border=True):
                if st.button(
                    "Load New Sentence",
                    use_container_width=True,
                ):
                    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    st.session_state.pop("pending_user_input", None)
                    sample = random.choice(rows)
                    st.session_state.random_sample = sample
                    sentence_text = sample.get("sentence") or sample.get("text") or ""
                    if sentence_text:
                        st.session_state.pending_user_input = sentence_text
                        st.rerun()
                progress_placeholder = st.empty()

        pending_user_input = st.session_state.pop("pending_user_input", None)
        user_input = pending_user_input
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            if progress_placeholder is not None:
                with progress_placeholder.container():
                    progress = st.progress(0, text="Analyzing...")
                    progress_value = 0
                    for _ in stream_assistant_response():
                        progress_value = min(progress_value + 5, 95)
                        progress.progress(progress_value, text="Analyzing...")
                    progress.progress(100, text="Complete")
                progress_placeholder.empty()
            else:
                for _ in stream_assistant_response():
                    pass

        latest_user_sentence = get_latest_message_content("user")
        latest_assistant_analysis = get_latest_message_content("assistant")

        with left_col:
            with st.container(border=True):
                st.subheader("Dataset Sentence")
                if latest_user_sentence:
                    st.markdown(latest_user_sentence)
                elif sample:
                    fallback_sentence = sample.get("sentence") or sample.get("text") or ""
                    st.markdown(fallback_sentence)
                else:
                    st.info("Load a sentence to begin.")

            with st.container(border=True):
                st.metric("Dataset Sentiment Label", dataset_label)

        with right_col:
            with st.container(border=True):
                st.subheader("Model Analysis")
                if latest_assistant_analysis:
                    st.markdown(latest_assistant_analysis)
                else:
                    st.info("Analysis will appear here after loading a sentence.")


if __name__ == "__main__":
    main()
