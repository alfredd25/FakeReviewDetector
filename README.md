# 🕵️‍♂️ Fake Review Detector

A Chrome extension that uses Machine Learning to detect and highlight potentially fake reviews on platforms like **Amazon** and **TripAdvisor**.

---

## 🚀 Features

- ✅ **Automatic Review Scanning**  
  Injects into supported websites and scans all visible reviews

- ✅ **Color-Coded Highlights**
  - 🟥 **Red**: Fake review detected
  - 🟩 **Green**: Real review with high confidence (≥ 70%)
  - 🟨 **Yellow**: Real review with low confidence (< 70%)

- ✅ **Manual Review Checker**  
  Use the extension popup to test any review manually

---

## 🧠 Architecture

This project consists of two main components:

### 1. Machine Learning Backend
- Python-based Flask API
- Trained using a Naive Bayes classifier on public TripAdvisor fake review datasets
- Hosted publicly on **Render** for live analysis

### 2. Chrome Extension
- Injects a content script that:
  - Identifies review blocks
  - Sends text to the Flask API
  - Highlights reviews based on predictions

---

## 🔧 Tech Stack

| Component        | Tech Used                     |
|------------------|-------------------------------|
| **Backend (ML)** | Python, Flask, scikit-learn, NLTK, joblib |
| **Frontend (Ext)** | JavaScript, HTML, CSS (Chrome Extension API) |
| **Hosting**      | [Render](https://render.com) (Free Tier) |
| **Dataset**      | [TripAdvisor Deceptive Opinion Spam Corpus](https://myleott.com/op_spam/) |

---

## 🌍 Supported Sites

- ✅ [Amazon.in](https://www.amazon.in/)
- ✅ [TripAdvisor.com](https://www.tripadvisor.com/)
- ❌ (Others coming soon)

---

## 🛠️ Setup & Installation (For Developers)

### 🧩 Load Extension Locally

1. Clone or download this repo
2. Go to `chrome://extensions`
3. Enable **Developer Mode**
4. Click **Load Unpacked**
5. Select the `extension/` folder

### 🧪 Run Backend Locally (Optional)
cd backend
pip install -r requirements.txt
python predict.py


### 📈 Project Status
✅ MVP Complete
✅ Live API deployed
🚧 All-site support in progress
🚧 Chrome Web Store publishing in progress

📄 License
This project is licensed under the MIT License — see the LICENSE file for details.
