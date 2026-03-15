from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import time

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL = "https://router.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "token_set": bool(HF_TOKEN)
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    output = None

    for attempt in range(5):  # increased to 5 — model cold start takes time
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=30)
            print(f"Attempt {attempt+1} | Status: {response.status_code}")
            output = response.json()
            print(f"HF Output: {output}")  # THIS is the key line — you'll see it in Render logs now

            if isinstance(output, dict) and "error" in output:
                if "loading" in output["error"].lower():
                    print(f"Model loading, waiting 10s...")
                    time.sleep(10)
                    continue
                else:
                    return jsonify({"error": output["error"]}), 500

            # Valid response — break out
            break

        except Exception as e:
            print(f"Exception on attempt {attempt+1}: {str(e)}")
            return jsonify({"error": f"Request to HuggingFace failed: {str(e)}"}), 500

    if output is None:
        return jsonify({"error": "HuggingFace model did not respond after 5 attempts"}), 500

    try:
        if isinstance(output[0], list):
            result = output[0][0]
        else:
            result = output[0]

        return jsonify({"label": result["label"], "score": round(result["score"] * 100, 2)})

    except (IndexError, KeyError, TypeError) as e:
        print(f"Parse error: {str(e)} | Raw output was: {output}")
        return jsonify({"error": f"Unexpected HF response format: {str(output)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)