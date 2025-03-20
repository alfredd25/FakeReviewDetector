import pandas as pd
import os
import re
from sklearn.model_selection import train_test_split


def load_hotel_reviews(directory):
    data = []

    polarities = ['positive_polarity', 'negative_polarity']
    sources = ['deceptive_from_MTurk', 'truthful_from_Web']

    for polarity in polarities:
        polarity_path = os.path.join(directory, polarity)
        if not os.path.exists(polarity_path):
            print(f"Warning: Polarity directory not found: {polarity_path}")
            continue

        for source in sources:
            is_fake = 'deceptive' in source
            label = 'fake' if is_fake else 'real'

            source_dir = os.path.join(polarity_path, source)

            if not os.path.exists(source_dir):
                print(f"Warning: Source directory not found: {source_dir}")
                continue

            for fold in os.listdir(source_dir):
                fold_path = os.path.join(source_dir, fold)

                if os.path.isdir(fold_path):
                    for file in os.listdir(fold_path):
                        if file.endswith('.txt'):
                            file_path = os.path.join(fold_path, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    review_text = f.read()
                                    data.append({
                                        'text': review_text,
                                        'label': label,
                                        'polarity': polarity,
                                        'source': source,
                                        'fold': fold,
                                        'file': file
                                    })
                            except Exception as e:
                                print(f"Error reading {file_path}: {e}")

    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} reviews")
    print(f"Label distribution: {df['label'].value_counts().to_dict()}")

    return df


def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return ''


def extract_features(df):
    df['clean_text'] = df['text'].apply(clean_text)

    df['review_length'] = df['text'].apply(len)
    df['word_count'] = df['text'].apply(lambda x: len(x.split()))
    df['capitals_ratio'] = df['text'].apply(
        lambda x: sum(1 for c in x if c.isupper()) / len(x) if len(x) > 0 else 0
    )

    return df


def prepare_dataset():
    df = load_hotel_reviews('../datasets/Hotel_reviews')

    df = extract_features(df)

    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df['label']
    )

    df.to_csv('../datasets/hotel_reviews_all.csv', index=False)
    train_df.to_csv('../datasets/hotel_reviews_train.csv', index=False)
    test_df.to_csv('../datasets/hotel_reviews_test.csv', index=False)

    print(f"Full dataset size: {len(df)}")
    print(f"Training set size: {len(train_df)}")
    print(f"Test set size: {len(test_df)}")

    return df, train_df, test_df


if __name__ == "__main__":
    prepare_dataset()

