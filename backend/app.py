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

    print("HF Status:", response.status_code)
    print("HF Response:", response.text)

    output = response.json()

    if isinstance(output, dict) and "error" in output:
        return jsonify({"error": output["error"]}), 500

    result = output[0][0]
    return jsonify({
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
