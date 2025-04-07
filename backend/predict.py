import os
import re
from flask import Flask, request, jsonify
import joblib
from scipy.sparse import hstack, csr_matrix

app = Flask(__name__)

model_dir = os.path.join(os.path.dirname(__file__), "model")
classifier = joblib.load(os.path.join(model_dir, "classifier.pkl"))
tfidf_vectorizer = joblib.load(os.path.join(model_dir, "vectorizer.pkl"))

def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return ''

def extract_metadata(text):
    review_length = len(text)
    word_count = len(text.split())
    capitals_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
    return [review_length, word_count, capitals_ratio]

def prepare_features(text):
    clean = clean_text(text)
    X_text = tfidf_vectorizer.transform([clean])
    meta_features = extract_metadata(text)
    X_meta = csr_matrix([meta_features])
    return hstack([X_text, X_meta])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'review' not in data:
        return jsonify({'error': 'No review provided'}), 400

    review_text = data['review'].strip()
    if not review_text:
        return jsonify({'error': 'Empty review text'}), 400

    try:
        X = prepare_features(review_text)
        pred = classifier.predict(X)[0]
        proba = classifier.predict_proba(X)[0]
        confidence = max(proba)
        return jsonify({'label': pred, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/predict-batch", methods=["POST"])
def predict_batch():
    data = request.get_json()
    if not data or "reviews" not in data:
        return jsonify({"error": "No reviews provided"}), 400
    reviews = data["reviews"]
    results = []
    for review in reviews:
        X = prepare_features(review)
        pred = classifier.predict(X)[0]
        proba = classifier.predict_proba(X)[0]
        confidence = max(proba)
        results.append({"review": review, "label": pred, "confidence": confidence})
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
