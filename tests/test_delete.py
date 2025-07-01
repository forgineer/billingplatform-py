import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


class TestBillingPlatformDelete(unittest.TestCase):
    def test_basic_delete(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        # Single record deletion
        payload: dict = {
            'Id': '12345' 
        }
        response: dict = bp.delete(entity='ACCOUNT', data=payload)

        # Multiple records deletion
        payload: list[dict] = [
            {
                'Id': '12345'
            },
            {
                'Id': '67890'
            }
        ]
        response: dict = bp.delete(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)

    def test_brmobject_delete(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        payload: dict = {
            'brmObjects': {
                'Id': '12345' # Example ID, replace with a valid one
            }
        }

        response: dict = bp.delete(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)


if __name__ == '__main__':
    unittest.main()
