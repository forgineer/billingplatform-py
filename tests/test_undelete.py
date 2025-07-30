import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


"""
Tests assume an existing credentials file in the root directory. For more information of the expected format, 
see the utils_for_testing.py file.
"""

class TestBillingPlatformDelete(unittest.TestCase):
    def test_basic_undelete(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        # Single record undelete
        payload: dict = {
            'Id': '12345' 
        }
        response: dict = bp.undelete(entity='ACCOUNT', data=payload)

        # Multiple records undelete
        payload: list[dict] = [
            {
                'Id': '12345'
            },
            {
                'Id': '67890'
            }
        ]
        response: dict = bp.undelete(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)

    def test_brmobject_undelete(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        payload: dict = {
            'brmObjects': {
                'Id': '12345' # Example ID, replace with a valid one
            }
        }

        response: dict = bp.undelete(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)


if __name__ == '__main__':
    unittest.main()
