from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
from scraper import fetch_html

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

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