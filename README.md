# Sentiment Analyzer — Full Stack AI Web App

A full stack web application that analyzes the sentiment of any text using AI.

## Live Demo
🔗 [Frontend](#) | [Backend API](#)
*(links coming after deployment)*

## What It Does
- User enters any text
- App sends it to a Python Flask backend via REST API
- Backend runs it through HuggingFace's distilbert AI model
- Returns Positive/Negative classification with confidence score
- Result displays instantly with color coding

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React |
| Backend | Python Flask |
| AI Model | HuggingFace distilbert-base-uncased-finetuned-sst-2-english |
| Deployment | Vercel (frontend) + Render (backend) |

## How To Run Locally

### Backend
```bash
cd backend
pip install flask flask-cors transformers torch
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Background
This project is an upgraded version of a sentiment analysis classifier
I originally built in undergrad using NLTK and Naive Bayes. This version
uses a modern transformer model, full stack architecture, and live deployment.

## Author
Soham Dhuri | [LinkedIn](https://linkedin.com/in/soham-s-dhuri)
```

**Step 4 — Save it, then push to GitHub:**
```
git add .
git commit -m "Add project README"
git push