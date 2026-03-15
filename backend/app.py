from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import time

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL = "https://router.huggingface.co/hf-inference/models/distilbert-base-uncased-finetuned-sst-2-english"

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "token_set": bool(HF_TOKEN)
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        headers = {"Authorization": f"Bearer {HF_TOKEN}"}

        for attempt in range(5):
            print(f"=== Attempt {attempt+1} ===")
            
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": text},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Body: {response.text[:300]}")

            if response.status_code != 200:
                print(f"Non-200 response, retrying...")
                time.sleep(5)
                continue

            output = response.json()
            print(f"Parsed output: {output}")

            if isinstance(output, dict) and "error" in output:
                if "loading" in output["error"].lower():
                    print("Model loading, waiting 10s...")
                    time.sleep(10)
                    continue
                return jsonify({"error": output["error"]}), 500

            # Success — parse result
            if isinstance(output[0], list):
                result = output[0][0]
            else:
                result = output[0]

            return jsonify({
                "label": result["label"],
                "score": round(result["score"] * 100, 2)
            })

        return jsonify({"error": "HuggingFace did not respond after 5 attempts"}), 500

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)