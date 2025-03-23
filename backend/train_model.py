import os
import pandas as pd
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def load_data(train_path, test_path):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def build_feature_matrix(train_df, test_df, max_features=5000):
    tfidf_vectorizer = TfidfVectorizer(max_features=max_features)

    X_train_text = tfidf_vectorizer.fit_transform(train_df["clean_text"])
    X_test_text = tfidf_vectorizer.transform(test_df["clean_text"])

    X_train_meta = csr_matrix(train_df[["review_length", "word_count", "capitals_ratio"]].values)
    X_test_meta = csr_matrix(test_df[["review_length", "word_count", "capitals_ratio"]].values)
    X_train = hstack([X_train_text, X_train_meta])

    X_test = hstack([X_test_text, X_test_meta])
    return X_train, X_test, tfidf_vectorizer

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    train_csv = os.path.join(base_dir, 'datasets', 'hotel_reviews_train.csv')
    test_csv = os.path.join(base_dir, 'datasets', 'hotel_reviews_test.csv')
    train_df, test_df = load_data(train_csv, test_csv)

    X_train, X_test, tfidf_vectorizer = build_feature_matrix(train_df, test_df)
    y_train = train_df["label"]
    y_test = test_df["label"]

    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print("Accuracy on test set: {:.2f}%".format(acc * 100))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    model_dir = os.path.join(os.path.dirname(__file__), "model")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(clf, os.path.join(model_dir, "classifier.pkl"))
    joblib.dump(tfidf_vectorizer, os.path.join(model_dir, "vectorizer.pkl"))
    print("Model and Vectorizer saved in", model_dir)


if __name__ == "__main__":
    main()
