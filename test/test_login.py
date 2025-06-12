import logging
import requests
import unittest

from billingplatform import BillingPlatform


class TestBillingPlatformLogin(unittest.TestCase):
    def test_session_login(self):
        logging.basicConfig(level=logging.DEBUG)
        
        # Fake credentials for testing against the mock server
        session_credentials = {
            'base_url': 'http://localhost',
            'username': 'blake',
            'password': 'passwd'
        }
        bp = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)


if __name__ == '__main__':
    unittest.main()