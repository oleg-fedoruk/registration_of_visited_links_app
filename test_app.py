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
        data_to_send = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
        first_json = json.dumps(data_to_send)
        response = self.app.post(self.base_url, data=first_json)
        response_text = response.data.decode()
        self.assertEqual('{"status": "ok"}', response_text)

    def test_post_with_invalid_data(self):
        data_to_send = '["krollykin.ru"]'
        response = self.app.post(self.base_url, data=data_to_send)
        response_text = response.data.decode()
        self.assertEqual("Invalid data. Your JSON don't have key 'links'", response_text)

    def test_post_without_links_key(self):
        data_to_send = '{"cell": ["krollykin.ru"]}'
        response = self.app.post(self.base_url, data=data_to_send)
        response_text = response.data.decode()
        self.assertEqual("Invalid data. Key 'links' is empty or your JSON don't have such key", response_text)

    def test_post_without_value_of_links_key(self):
        data_to_send = '{"links": []}'
        response = self.app.post(self.base_url, data=data_to_send)
        response_text = response.data.decode()
        self.assertEqual("Invalid data. Key 'links' is empty or your JSON don't have such key", response_text)


class TestGetRequest(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/visited_domains'
        self.fill_database()

    def fill_database(self):
        data_to_send = [{
            "links": [
                "funbox.ru"
            ]
        },
            {
                "links": [
                    "funbox.ru"
                ]
            },
            {
                "links": [
                    "yandex.ru"
                ]
            }
        ]
        for data in data_to_send:
            serilized_data = json.dumps(data)
            self.app.post('/visited_links', data=serilized_data)
            time.sleep(1)

    def test_get_request_return_uniq_urls(self):
        now = int(time.time())
        time_from = now - 4
        my_req = f'?from={time_from}&to={now}'
        response = self.app.get(self.base_url + my_req)
        response_text = response.data.decode()
        serilized_response = '{"domains": ["funbox.ru", "yandex.ru"], "status": "ok"}'
        self.assertEqual(response_text, serilized_response)

    def test_get_request_return_filtered_result(self):
        now = int(time.time())
        time_from = now - 1
        my_req = f'?from={time_from}&to={now}'
        response = self.app.get(self.base_url + my_req)
        response_text = response.data.decode()
        serilized_response = '{"domains": ["yandex.ru"], "status": "ok"}'
        self.assertEqual(response_text, serilized_response)
