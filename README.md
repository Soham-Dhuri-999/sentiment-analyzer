# Sentiment Analyzer — Full Stack AI Web App

A full stack web application that analyzes the sentiment of any text using AI.

## Live Demo
🔗 [Frontend](https://sentiment-analyzer-kp93-8hs2khxwq-soham-dhuri-999s-projects.vercel.app) | [Backend API](https://sentiment-analyzer-backend-9uys.onrender.com)

> **Note:** Backend runs on Render's free tier and may take 15–20 seconds to wake up on first request. This is expected.

## What It Does
- User enters any text
- App sends it to a Python Flask backend via REST API
- Backend calls HuggingFace's distilbert model via the `huggingface_hub` SDK
- Returns Positive/Negative classification with confidence score
- Result displays instantly with color coding (green = positive, red = negative)

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React |
| Backend | Python Flask |
| AI Model | HuggingFace `distilbert/distilbert-base-uncased-finetuned-sst-2-english` |
| AI Integration | `huggingface_hub` InferenceClient SDK |
| Deployment | Vercel (frontend) + Render (backend) |

## How To Run Locally

### Prerequisites
- Python 3.8+
- Node.js 16+
- A HuggingFace account with an API token ([get one here](https://huggingface.co/settings/tokens))

### Backend
```bash
cd backend
pip install flask flask-cors huggingface_hub
export HF_TOKEN=your_huggingface_token_here
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000` | Backend runs on `http://localhost:5000`

## Project Structure
```
sentiment-analyzer/
├── backend/
│   ├── app.py          # Flask API with /analyze endpoint
│   └── requirements.txt
└── frontend/
    └── src/
        └── App.jsx     # React UI with fetch call to backend
```

## Background
This project is an upgraded version of a sentiment analysis classifier
I originally built in undergrad using NLTK and Naive Bayes. This version
uses a modern transformer model via HuggingFace, full stack architecture,
and live cloud deployment — built and debugged end to end.

## Author
Soham Dhuri | [LinkedIn](https://linkedin.com/in/soham-s-dhuri) | [GitHub](https://github.com/Soham-Dhuri-999)