from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
from scraper import fetch_html

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route("/scrape", methods=["POST"])
def scrape_with_scraperapi():
    import os
    import requests

    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL não fornecida"}), 400

    SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")
    if not SCRAPERAPI_KEY:
        return jsonify({"error": "SCRAPERAPI_KEY não configurada"}), 500

    api_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={url}"

    try:
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200 and "html" in response.headers.get("Content-Type", ""):
            return jsonify({"success": True, "html_length": len(response.text)})
        return jsonify({"success": False, "status_code": response.status_code, "content": response.text[:200]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL não fornecida"}), 400
    html = fetch_html(url)
    if html:
        return jsonify({"success": True, "length": len(html)})
    return jsonify({"success": False, "error": "Falha ao obter HTML"})
