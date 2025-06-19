import logging
import requests
import unittest

from billingplatform import BillingPlatform


def get_credentials(path='credentials.json') -> dict:
    """
    Load credentials from a JSON file.
    """
    import json
    
    with open(path) as f:
        return json.load(f)


class TestBillingPlatformQuery(unittest.TestCase):
    def test_basic_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        data: dict = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1")
        #print(data)

        self.assertIsInstance(data, dict)


if __name__ == '__main__':
    unittest.main()
