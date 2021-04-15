import unittest
import json

from unittest import TestCase
from unittest.mock import Mock, patch
from api.client import ApiClient
from api.exception import APIException


class TestApiClient(TestCase):
    @patch('api.client.requests.get')
    def test_execute_get_success(self, request_mock):
        api_response_fixture = {'product_id': 'opnsense'}
        request_mock.return_value.status_code = 200
        request_mock.return_value.text = json.dumps(api_response_fixture)

        client_args = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]
        api_config = {
            "module": "Core",
            "controller": "firmware",
            "method": "get",
            "command": "info",
        }
        api_parameters = []

        client = ApiClient(*client_args)
        result = client.execute(*api_parameters, **api_config)

        request_mock.assert_called_once_with(
            'https://127.0.0.1/api/core/firmware/info',
            verify='~/.opn-cli/ca.pem',
            auth=('api_key', 'api_secret'),
            timeout=60
        )
        self.assertEqual(api_response_fixture, result)

    @patch('api.client.requests.get')
    def test_execute_get_failure(self, request_mock):
        request_mock.return_value.status_code = 400
        request_mock.return_value.text = {
            "message": "controller OPNsense\\Core\\Api\\IndexController not found",
            "status": 400
        }
        request_mock.return_value.url = 'https://127.0.0.1/api/not/existing/confusion'

        client_args = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]
        api_config = {
            "module": "Not",
            "controller": "Existing",
            "method": "get",
            "command": "confusion",
        }
        api_parameters = []

        client = ApiClient(*client_args)
        self.assertRaises(APIException, client.execute, *api_parameters, **api_config)
        request_mock.assert_called_once_with(
            'https://127.0.0.1/api/not/existing/confusion',
            verify='~/.opn-cli/ca.pem',
            auth=('api_key', 'api_secret'),
            timeout=60
        )


    @patch('api.client.requests.post')
    def test_execute_post_success(self, request_mock):
        api_response_fixture = [
            {'status': 'ok', 'msg_uuid': '8a0a415a-dbee-410d-be9f-01b90d71ff7c'}
        ]
        request_mock.return_value.status_code = 200
        request_mock.return_value.text = json.dumps(api_response_fixture)

        client_args = [
            'api_key2',
            'api_secret2',
            'https://127.0.0.1/api',
            False,
            '~/.opn-cli/ca.pem',
            40
        ]
        api_config = {
            "module": "Core",
            "controller": "Firmware",
            "method": "post",
            "command": "reinstall",
        }
        api_parameters = [
            'os_plugin_name'
        ]

        client = ApiClient(*client_args)
        result = client.execute(*api_parameters, **api_config)

        request_mock.assert_called_once_with(
            'https://127.0.0.1/api/core/firmware/reinstall/os_plugin_name',
            data=None,
            verify=False,
            auth=('api_key2', 'api_secret2'),
            timeout=40
        )
        self.assertEqual(api_response_fixture, result)

    def test_execute_failure(self):
        client_args = [
            'api_key3',
            'api_secret3',
            'https://127.0.0.1/api',
            False,
            '~/.opn-cli/ca.pem',
            10
        ]
        api_config = {
            "module": "Core",
            "controller": "Firmware",
            "method": "head",
            "command": "reinstall",
        }
        api_parameters = []

        client = ApiClient(*client_args)
        self.assertRaises(NotImplementedError, client.execute, *api_parameters, **api_config)


if __name__ == '__main__':
    unittest.main()
