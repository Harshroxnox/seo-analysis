from flask import Blueprint, request, jsonify
from services.seo_service import analyze_text, insert_keyword, get_keywords, get_word_density, get_metrics

seo_bp = Blueprint("seo", __name__)

# This route will give us analysis about the text using TextRazor
@seo_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = analyze_text(text)
    return jsonify(result)

# This route will give us metrics about the text using py-readability-metrics
@seo_bp.route("/metrics", methods=["POST"])
def metrics():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = get_metrics(text)
    return jsonify(result)

# This route will be used to suggest keywords about the text using llm gemini
@seo_bp.route("/keywords", methods=["POST"])
def keywords():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = get_keywords(text)
    return jsonify(result)

# This route will be used to calculate the percentage word density
@seo_bp.route("/word_density", methods=["POST"])
def word_density():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = get_word_density(text)
    return jsonify(result)

# This route will insert the keywords into the given text in a meaningful way using gemini-llm
@seo_bp.route("/insert", methods=["POST"])
def insert():
    data = request.json
    text = data.get("text", "")
    keyword = data.get("keyword", "")
    if not text or not keyword:
        return jsonify({"error": "Missing text or keyword"}), 400

    updated_text = insert_keyword(text, keyword)
    return jsonify({"updated_text": updated_text})
