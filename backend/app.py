from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HF_TOKEN = os.environ.get("HF_TOKEN", "")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": text}
    )

    output = response.json()

    # handle API errors safely
    if isinstance(output, dict) and "error" in output:
        return jsonify({"error": output["error"]}), 500

    label = output[0]["label"]
    score = round(output[0]["score"] * 100, 2)

    return jsonify({
        "label": label,
        "score": score
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
