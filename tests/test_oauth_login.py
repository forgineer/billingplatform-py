import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


"""
Tests assume an existing credentials file in the root directory. For more information of the expected format, 
see the utils_for_testing.py file.
"""

class TestBillingPlatformOAuthLogin(unittest.TestCase):
    def test_oauth_login(self):
        logging.basicConfig(level=logging.DEBUG)
        
        # Load OAuth credentials. Requesting the default access token.
        session_credentials = get_credentials('credentials.json', 'oauth')
        bp_access_token: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp_access_token, BillingPlatform)
        self.assertIsInstance(bp_access_token.session, requests.Session)

        # Load OAuth credentials. Requesting the refresh token.
        session_credentials = get_credentials('credentials.json', 'oauth')
        session_credentials.update({'use_token': 'refresh_token'}) # Override to use refresh token
        bp_refresh_token: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp_refresh_token, BillingPlatform)
        self.assertIsInstance(bp_refresh_token.session, requests.Session)


if __name__ == '__main__':
    unittest.main()