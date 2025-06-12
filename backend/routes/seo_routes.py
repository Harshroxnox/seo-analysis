from flask import Blueprint, request, jsonify
from services.seo_service import analyze_text, insert_keyword

seo_bp = Blueprint("seo", __name__)

@seo_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = analyze_text(text)
    return jsonify(result)

@seo_bp.route("/insert", methods=["POST"])
def insert():
    data = request.json
    text = data.get("text", "")
    keyword = data.get("keyword", "")
    if not text or not keyword:
        return jsonify({"error": "Missing text or keyword"}), 400

    updated_text = insert_keyword(text, keyword)
    return jsonify({"updated_text": updated_text})
