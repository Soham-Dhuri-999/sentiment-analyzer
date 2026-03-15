from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "token_set": bool(HF_TOKEN)})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        if not data or not data.get("text"):
            return jsonify({"error": "No text provided"}), 400

        result = client.text_classification(
            data["text"],
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        )
        top = result[0]
        return jsonify({"label": top.label, "score": round(top.score * 100, 2)})

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)