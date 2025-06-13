from readability import Readability
from flask import current_app
from google import genai
import textrazor
import re
from collections import Counter
import json
import os


def analyze_text(text):
    textrazor.api_key = current_app.config["TEXTRAZOR_API_KEY"]
    textrazor_client = textrazor.TextRazor(extractors=["entities", "topics", "words", "phrases"])
    
    response = textrazor_client.analyze(text)

    if not response.ok:
        return {"error": "TextRazor API error", "status": response.status_code}
    
    json_content = response.json
    json_content = json_content["response"]

    cleaned_data = {}

    cleaned_data["entities"] = [
        {
            "id" : ent["id"],
            "entityId" : ent["entityId"],
            "confidenceScore" : ent["confidenceScore"],
            "relevanceScore" : ent["relevanceScore"],
            "wikiLink" : ent["wikiLink"],
        }
        for ent in json_content["entities"]
    ]

    cleaned_data["coarseTopics"] = json_content["coarseTopics"]

    # Path to the JSON tagsets file
    json_path = os.path.join(os.path.dirname(__file__), '..', 'upenn_tagset.json')
    json_path = os.path.abspath(json_path)
    
    # Load JSON
    with open(json_path, 'r') as f:
        global tagset
        tagset = json.load(f)

    sentences = []
    for sentence in json_content["sentences"]:
        obj = {}
        obj["position"] = sentence["position"]
        obj["words"] = [
            {
                "token" : word["token"],
                "partOfSpeech" : tagset[word["partOfSpeech"]][0]
            }
            for word in sentence["words"]
        ]
        sentences.append(obj)

    cleaned_data["sentences"] = sentences

    cleaned_data["topics"] = [
        {
            "id" : topic["id"],
            "label" : topic["label"],
            "score" : topic["score"],
            "wikiLink" : topic["wikiLink"],
        }
        for topic in json_content["topics"][:15]
    ]

    return cleaned_data


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
