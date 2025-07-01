import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


class TestBillingPlatformUpdate(unittest.TestCase):
    def test_basic_update(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        # Single record update
        payload: dict = {
            'Id': '12345', # Example ID, replace with a valid one
            'Name': 'Test Account 1',
            'Status': 'ACTIVE'
        }
        response: dict = bp.update(entity='ACCOUNT', data=payload)

        # Multiple records update
        payload: list[dict] = [
            {
                'Id': '12345', # Example ID, replace with a valid one
                'Name': 'Test Account 1',
                'Status': 'ACTIVE'
            },
            {
                'Id': '67890', # Example ID, replace with a valid one
                'Name': 'Test Account 2',
                'Status': 'ACTIVE'
            }

        ]
        response: dict = bp.update(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)

    def test_brmobject_update(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        payload: dict = {
            'brmObjects': {
                'Id': '12345', # Example ID, replace with a valid one
                'Name': 'Test Account',
                'Status': 'ACTIVE'
            }
        }

        response: dict = bp.update(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)

if __name__ == '__main__':
    unittest.main()
