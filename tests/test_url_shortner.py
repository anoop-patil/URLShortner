from flask_testing import TestCase
from url_shortner import app
import redis


class TestURLShortening(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        # Override any other configurations for testing
        app.config["REDIS_DB"] = 10  # Use a different database index for tests
        return app

    def setUp(self):
        self.redis_client = redis.Redis(
            host="localhost", port=6379, db=app.config["REDIS_DB"]
        )
        self.redis_client.flushdb()

    def tearDown(self):
        pass

    def test_shorten_url(self):
        response = self.client.post("/", json={"url": "https://example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("short_url", response.json)
        self.assertIn("http://localhost/", response.json["short_url"])

    def test_redirect_to_original_url(self):
        long_url = "https://www.example.com"
        response = self.client.post("/", json={"url": long_url})
        short_key = response.json["key"]

        response = self.client.get(f"/{short_key}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, long_url)

    def test_delete_shortened_url(self):

        long_url = "https://www.example.com"
        response = self.client.post("/", json={"url": long_url})
        short_key = response.json["key"]

        response = self.client.delete(f"/{short_key}")

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/{short_key}")

        self.assertEqual(response.status_code, 404)
