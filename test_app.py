import unittest
from app import app


class AppTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_app_with_no_tag(self):
        response = self.app.get('/posts?direction=desc')
        self.assertEqual(response.status_code, 400)

    def test_app_with_invalid_sortBy(self):
        response = self.app.get('/posts?tags=history,tech&sortBy=avg')
        self.assertEqual(response.status_code, 400)

    def test_app_with_invalid_direction(self):
        response = self.app.get('/posts?tags=history,tech&sortBy=desc&direction=up')
        self.assertEqual(response.status_code, 400)

    def test_app_with_invalid_parameter(self):
        response = self.app.get('/posts?tags=history,tech&sortBy=desc&direction=up&olderThan=2021-06-05')
        self.assertEqual(response.status_code, 400)


if __name__=="__main__":
    unittest.main()
