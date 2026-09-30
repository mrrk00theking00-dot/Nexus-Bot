from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="static")
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

def analyze_emergency(text):
    prompt = f"""
You are an emergency response analysis system.

Analyze the following emergency text and produce:
1. A concise summary (max 4 lines)
2. The type of emergency
3. Immediate recommended actions

Emergency Text:
<<< {text} >>>

Respond strictly in this format:

Summary:
- ...

Emergency Type:
- ...

Immediate Actions:
- ...
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"]

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    emergency_text = data.get("text", "")

    if not emergency_text.strip():
        return jsonify({"error": "Empty input"}), 400

    result = analyze_emergency(emergency_text)
    return jsonify({"analysis": result})

if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)