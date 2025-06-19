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


class TestBillingPlatformLogin(unittest.TestCase):
    def test_session_login(self):
        logging.basicConfig(level=logging.DEBUG)
        
        session_credentials = get_credentials()
        bp = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)


if __name__ == '__main__':
    unittest.main()