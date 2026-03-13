from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

sentiment_model = pipeline("sentiment-analysis")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = sentiment_model(text)[0]
    return jsonify({
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)