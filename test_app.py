import json
import time

from main import app
from unittest import TestCase


class TestPostRequest(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/visited_links'

    def test_post_request(self):
        first = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
        first_json = json.dumps(first)
        response = self.app.post(self.base_url, data=first_json)
        response_text = response.data.decode()
        self.assertEqual('{"status": "ok"}', response_text)
