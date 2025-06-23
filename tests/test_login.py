import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


class TestBillingPlatformLogin(unittest.TestCase):
    def test_session_login(self):
        logging.basicConfig(level=logging.DEBUG)
        
        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)
    
    def test_logout(self):
        logging.basicConfig(level=logging.DEBUG)
        
        session_credentials = get_credentials()
        session_credentials.update({'logout_at_exit': False}) # Prevent automatic logout at exit
        # Review log to ensure that logout at exit is disabled
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        # Perform logout manually
        bp.logout()


if __name__ == '__main__':
    unittest.main()