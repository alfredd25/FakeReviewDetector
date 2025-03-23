import unittest
import json
from backend.predict import app

class TestPredictionAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_single_prediction(self):
        payload = {'review': 'This hotel has excellent service and a comfortable room.'}
        response = self.app.post('/predict', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('label', data)
        self.assertIn('confidence', data)

    def test_batch_prediction(self):
        payload = {
            'reviews': [
                'The room was dirty and the service was terrible.',
                'Had a wonderful stay with great amenities.'
            ]
        }
        response = self.app.post('/predict-batch', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        for result in data:
            self.assertIn('label', result)
            self.assertIn('confidence', result)

    def test_no_review(self):
        payload = {}
        response = self.app.post('/predict', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
