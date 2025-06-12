import os
import requests

# Simple analysis placeholder
def analyze_text(text):
    # You can connect to Twinword API here
    return {
        "readability_score": 75,
        "suggested_keywords": ["focus", "routine", "discipline"],
        "seo_opportunities": ["Shorten long sentences", "Add headings"]
    }

# Naive keyword insertion
def insert_keyword(text, keyword):
    sentences = text.split('.')
    for i, sentence in enumerate(sentences):
        if keyword.lower() not in sentence.lower():
            sentences[i] = sentence.strip() + f" {keyword.capitalize()} helps with this"
            break
    return '. '.join(sentences) + '.'
