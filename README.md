# 🎙️ AI-Generated Voice Detection API

This project is an **AI-powered REST API** built for the **GUVI × HCL Hackathon**, designed to detect whether a given voice sample is **AI-generated** or **spoken by a real human**.

The solution supports **multiple Indian languages** and follows all hackathon requirements, including **Base64 audio input**, **JSON output**, and **confidence scoring**.

---

## 🚀 Problem Statement

With the rapid growth of AI-generated voices and voice cloning, audio deepfakes are increasingly used for fraud, impersonation, and misinformation.

This project provides an automated system that:
- Analyzes a voice sample
- Detects whether it is **AI-generated** or **Human**
- Returns a structured JSON response with a confidence score

---

## 🧠 Solution Overview

The system follows an end-to-end AI pipeline:

1. Accepts **Base64-encoded MP3 audio** via REST API  
2. Decodes and preprocesses the audio  
3. Extracts acoustic features (spectral & temporal)  
4. Performs AI-based classification  
5. Returns prediction with confidence score  

---

## 🌐 Supported Languages

- Tamil  
- English  
- Hindi  
- Malayalam  
- Telugu  

---

## ✨ Features

- REST API-based architecture  
- Base64 audio input support  
- Multilingual voice detection  
- AI-generated vs Human classification  
- Confidence score between `0.0` and `1.0`  
- Structured JSON response  
- Hackathon-compliant design  

---

## 📁 Project Structure

ai-voice-detection/
│
├── backend/ # REST API and AI inference logic
├── frontend/ # Optional UI for testing
├── encode_audio.py # Utility for Base64 audio encoding
├── .gitignore
└── README.md


---

## ⚙️ Tech Stack

- **Backend**: Python (Flask / FastAPI)  
- **Audio Processing**: Librosa, NumPy  
- **Machine Learning**: Scikit-learn / TensorFlow / PyTorch  
- **API Format**: REST + JSON  

---

## 🔌 API Specification

### Endpoint
POST /detect-voice


### Headers
Content-Type: application/json
x-api-key: hackathon-secret-key


---

## 🧪 Hackathon Evaluation Alignment

- No hard-coded outputs  
- No external detection APIs  
- AI-based inference logic  
- Structured JSON output  
- Accuracy, stability, and explainability focused  

---

## 📌 Use Cases

- AI voice fraud detection  
- Deepfake audio identification  
- Secure voice authentication  
- Research and experimentation  

---

## 🚧 Future Improvements

- Real-time voice detection  
- Confidence visualization  
- Expanded multilingual support  
- Explainable AI predictions  
- Admin dashboard for analytics  

---

## 🏁 Hackathon Submission

This project was developed and submitted as part of the **GUVI × HCL Hackathon** under the problem statement:

**“AI-Generated Voice Detection (Tamil, English, Hindi, Malayalam, Telugu)”**
