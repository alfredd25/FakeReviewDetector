import unittest
import joblib
import os
from backend.predict import app, prepare_features

class TestFakeReviewDetector(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.model_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model')
        self.classifier = joblib.load(os.path.join(self.model_dir, 'classifier.pkl'))
        self.vectorizer = joblib.load(os.path.join(self.model_dir, 'vectorizer.pkl'))

    def test_model_prediction_real(self):
        review = "The hotel was clean and the staff were very helpful."
        X = prepare_features(review)
        prediction = self.classifier.predict(X)[0]
        self.assertIn(prediction, ['real', 'fake'])

    def test_model_prediction_fake(self):
        review = "I loved it! Best place ever! A++++ would go again!!!"
        X = prepare_features(review)
        prediction = self.classifier.predict(X)[0]
        self.assertIn(prediction, ['real', 'fake'])

    def test_flask_predict_api(self):
        response = self.app.post('/predict', json={'review': 'Absolutely horrible stay. Would not recommend.'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('label', data)
        self.assertIn('confidence', data)

    def test_flask_batch_predict_api(self):
        reviews = ["The food was amazing and the view was breathtaking.", "Terrible service and dirty rooms."]
        response = self.app.post('/predict-batch', json={'reviews': reviews})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        for result in data:
            self.assertIn('label', result)
            self.assertIn('confidence', result)

if __name__ == '__main__':
    unittest.main()
