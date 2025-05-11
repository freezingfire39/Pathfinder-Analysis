import unittest
import requests


class APITestConfig:
    """
    Simple configuration using curl-like command format
    """
    TEST_CASES = [
        {
            'name': 'analysis_endpoint',
            'method': 'POST',
            'url': 'http://127.0.0.1:8000/api/v1/py/analysis/',
            'headers': {
                'Content-Type': 'application/json'
            },
            'data': {
                'symbols': ['000001'],
                'method': 'max_sharpe_ratio',
                'amount': 1e6
            },
            'expected_status': 200,
            'response_validation': lambda r: isinstance(r, dict)
        },
        {
            'name': 'custom_portfolio_endpoint',
            'method': 'POST',
            'url': 'http://127.0.0.1:8000/api/v1/py/custom/portfolio/',
            'headers': {
                'Content-Type': 'application/json'
            },
            'data': {
                "weights": [{"symbol": "000001", "weight": 0.1}, {"symbol": "000003", "weight": 0.9}],
                "amount": 1e6
            },
            'expected_status': 200,
            'response_validation': lambda r: isinstance(r, dict)
        },
        {
            'name': 'timing_endpoint',
            'method': 'GET',
            'url': 'http://127.0.0.1:8000/api/v1/py/timing/',
            'headers': {
                'Content-Type': 'application/json'
            },
            # No data/params needed for this endpoint
            'expected_status': 200,
            'response_validation': lambda response: (
                isinstance(response, list) and  # Must be a list
                len(response) > 0 and  # Not empty
                all(isinstance(item, dict) for item in response) and  # All elements are dicts
                all('trade_date' in item and isinstance(item['trade_date'], str) for item in response) and  # Has date field
                all('close_sh' in item and isinstance(item['close_sh'], (int, float)) for item in response)  # Has numeric field
            )
        }
        ,
        {
            'name': 'default_portfolio_endpoint',
            'method': 'GET',
            'url': 'http://127.0.0.1:8000/api/v1/py/default/portfolio/',
            'headers': {
                'Content-Type': 'application/json'
            },
            # No data/params needed for this endpoint
            'expected_status': 200,
            'response_validation': lambda response: (
                    len(response) > 0   # Not empty
            )
        }
    ]


class TestAPI(unittest.TestCase):
    """
    Test case that automatically generates tests from the configuration
    """

    @classmethod
    def setUpClass(cls):
        cls.config = APITestConfig()

    def generate_test(test_case):
        """
        Dynamically generate test methods for each test case
        """

        def test_method(self):
            # Prepare request arguments
            kwargs = {
                'method': test_case['method'],
                'url': test_case['url'],
                'headers': test_case.get('headers', {})
            }

            # Only add json/data for non-GET requests
            if test_case['method'].upper() != 'GET' and 'data' in test_case:
                kwargs['json'] = test_case['data']

            # Make the request
            response = requests.request(**kwargs)

            # Verify status code
            self.assertEqual(response.status_code, test_case['expected_status'],
                             f"Status code mismatch for {test_case['name']}")

            # Verify content type if specified
            if 'headers' in test_case and 'Content-Type' in test_case['headers']:
                expected_content_type = test_case['headers']['Content-Type']
                self.assertIn(expected_content_type, response.headers['Content-Type'],
                              f"Content-Type mismatch for {test_case['name']}")

            # Parse response if JSON
            response_data = None
            if 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    response_data = response.json()
                except ValueError:
                    self.fail(f"Invalid JSON response for {test_case['name']}")

            # Run custom validation if provided
            if 'response_validation' in test_case and response_data is not None:
                self.assertTrue(test_case['response_validation'](response_data),
                                f"Response validation failed for {test_case['name']}")

        return test_method


# Dynamically create test methods for each test case
for test_case in APITestConfig.TEST_CASES:
    test_method = TestAPI.generate_test(test_case)
    setattr(TestAPI, f'test_{test_case["name"]}', test_method)

if __name__ == '__main__':
    unittest.main()