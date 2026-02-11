import os
import gradio as gr
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

key = os.getenv("AZURE_LANGUAGE_KEY")
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")

credential = AzureKeyCredential(key)
client = TextAnalyticsClient(endpoint, credential)

def analyze_text(text):
    if not text.strip():
        return "Please enter some text."

    # Language detection
    lang = client.detect_language([text])[0].primary_language.name

    # Sentiment
    sentiment_result = client.analyze_sentiment([text])[0]
    sentiment = sentiment_result.sentiment

    # Key phrases
    phrases = client.extract_key_phrases([text])[0].key_phrases

    # Entities
    entity_result = client.recognize_entities([text])[0]
    entities = [f"{e.text} ({e.category})" for e in entity_result.entities]

    return f"""
Language: {lang}

Sentiment: {sentiment}

Key Phrases: {phrases}

Entities: {entities}
"""

demo = gr.Interface(
    fn=analyze_text,
    inputs=gr.Textbox(lines=6, placeholder="Enter text here..."),
    outputs="text",
    title="AI Text Insight Analyzer (Azure AI)",
    description="Analyze sentiment, language, key phrases, and entities using Azure AI Language."
)

if __name__ == "__main__":
    demo.launch()
