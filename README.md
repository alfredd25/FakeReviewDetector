 
# Fake Review Detector

A Chrome extension that uses Machine Learning to detect and highlight potentially fake reviews on platforms like Amazon, Yelp, and TripAdvisor.

## Features

- Automatically scans and analyzes reviews on supported websites
- Highlights potentially fake reviews with color indicators:
  - **Red**: High confidence (90%+) that the review is fake
  - **Orange**: Uncertain but suspicious reviews
  - **Green**: Verified as genuine with high confidence.
- Provides a popup interface to manually check specific reviews

## Architecture

This project consists of two main components:

1. **Machine Learning Backend**: A Naive Bayes classifier trained on datasets of real and fake reviews, exposed via Flask API.
2. **Chrome Extension**: Injects JavaScript to identify, process, and highlight reviews based on the ML model's predictions.

## Project Status

🚧 Currently in development 🚧

## Technical Stack

- **Machine Learning**: Python, scikit-learn, NLTK, Flask
- **Extension**: JavaScript, HTML, CSS
- **Data**: Public review datasets from Yelp, Amazon, and TripAdvisor

## Getting Started

Instructions for setup and installation coming soon.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
