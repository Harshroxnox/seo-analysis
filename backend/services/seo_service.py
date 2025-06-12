from readability import Readability
from flask import current_app
from google import genai
import textrazor
import re
from collections import Counter


def analyze_text(text):
    textrazor.api_key = current_app.config["TEXTRAZOR_API_KEY"]
    textrazor_client = textrazor.TextRazor(extractors=["entities", "topics", "words", "phrases"])
    
    response = textrazor_client.analyze(text)

    if not response.ok:
        return {"error": "TextRazor API error", "status": response.status_code}
    
    json_content = response.json

    return json_content["response"]


def get_metrics(text):
    r = Readability(text)

    return {
        "flesch_kincaid": r.flesch_kincaid().score,
        "flesch": r.flesch().score,
        "gunning_fog": r.gunning_fog().score,
        "coleman_liau": r.coleman_liau().score,
        "dale_chall": r.dale_chall().score,
        "ari": r.ari().score,
        "linsear_write": r.linsear_write().score,
        "spache": r.spache().score,
    }


def get_keywords(text):
    gemini_api_key = current_app.config["GEMINI_API_KEY"]
    gemini_client = genai.Client(api_key=gemini_api_key)

    prompt = f"Extract the main keywords from the following text:\n\n{text}\n\nOnly return the keywords, separated by commas."
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt
    )

    return {
        "keywords" : response.text.strip()
    }



def get_word_density(text):
    # Normalize text: lowercase and extract words only
    words = re.findall(r'\b\w+\b', text.lower())

    total_words = len(words)
    word_counts = Counter(words)

    # Calculate density as a percentage
    density = {
        word: round((count / total_words) * 100, 2)
        for word, count in word_counts.items()
    }

    return density


def insert_keywords(text, keywords):
    gemini_api_key = current_app.config["GEMINI_API_KEY"]
    gemini_client = genai.Client(api_key=gemini_api_key)

    prompt = (
        f"Insert the following keywords naturally and meaningfully into the given text:\n"
        f"Keywords: {keywords}\n\n"
        f"Text: {text}\n\n"
        f"Return the updated text with all keywords smoothly integrated."
    )

    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return {
        "updated_text": response.text.strip()
    }
