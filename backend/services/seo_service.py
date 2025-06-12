import os
import requests


def analyze_text(text):
    print(os.environ.get("GEMINI_API_KEY"))
    return {
        "readability_score": 75,
        "suggested_keywords": ["focus", "routine", "discipline"],
        "seo_opportunities": ["Shorten long sentences", "Add headings"]
    }


def get_metrics(text):
    return {
        "flesch_kincaid": 75,
        "gunning_fog": 50
    }


def get_keywords(text):
    return ["baseball", "football", "cricket"]


def get_word_density(text):
    return {
        "The": 20,
        "cricket": 4.5,
        "hello": 9,
        "why" : 12,
        "baseball" : 4.5,
        "how": 50
    }


def insert_keyword(text, keyword):
    sentences = text.split('.')
    for i, sentence in enumerate(sentences):
        if keyword.lower() not in sentence.lower():
            sentences[i] = sentence.strip() + f" {keyword.capitalize()} helps with this"
            break
    return '. '.join(sentences) + '.'
