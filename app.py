import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from utils import extract_text_from_pdf

# Load environment variables
load_dotenv()

st.write("KEY FOUND:", bool(os.getenv("OPENAI_API_KEY")))
st.write("KEY PREFIX:", os.getenv("OPENAI_API_KEY")[:8])


# Create OpenAI client
client = OpenAI()

st.set_page_config(page_title="AI Document Summarizer", layout="centered")

st.title("📄 AI Document Summarizer")
st.write("Upload a document and get an AI-generated summary")

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])


def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful document summarizer."},
            {"role": "user", "content": f"Summarize the following document clearly and concisely:\n{text}"}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

    st.subheader("Extracted Text")
    st.text_area("Document Content", text, height=250)
st.markdown("---")
st.caption("Built using Streamlit + OpenAI")    