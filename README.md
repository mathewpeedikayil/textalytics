# Textalytics

Textalytics is a sentiment analysis project built with Python, Streamlit, and the Groq API (OpenAI-compatible client).

It loads random labeled sentences from a dataset, runs model analysis, and displays:
- dataset sentence
- dataset sentiment label (positive/negative)
- model analysis output (sentiment, tone, summary, evidence, confidence)

## Features

- Streamlit web interface for sentiment analysis
- Random sentence sampling from dataset
- Side-by-side dataset sentence and model analysis
- CLI chatbot script for terminal-based interaction

## Project Structure

- `app.py` - Streamlit app (main UI)
- `bot.py` - CLI chatbot script
- `data/` - Dataset files (`.txt`, `.csv`, `combined.csv`)
- `data.py` - Utility script to build CSV files
- `requirements.txt` - Python dependencies

## Setup

1. Clone the repository and move into the project folder.
2. Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Streamlit App

```bash
streamlit run app.py
```

## Run the CLI Bot

```bash
python bot.py
```

## Dataset

This project uses the **Sentiment Labelled Sentences** dataset from UCI:

- UCI dataset page: https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences
- Source domains: IMDb, Amazon, and Yelp
- Labels:
  - `1` -> `positive`
  - `0` -> `negative`

The dataset is associated with:

> Kotzias et al., *From Group to Individual Labels using Deep Features* (KDD 2015)

## Notes

- The app expects `data/combined.csv` to exist.
- Built with AI-assisted development support (GPT-5.3-Codex), with final implementation and testing by the author.
