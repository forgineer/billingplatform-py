import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


class TestBillingPlatformCreate(unittest.TestCase):
    def test_basic_create(self):
        """Test basic create functionality of BillingPlatform API."""
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        payload: dict = {
            'Name': 'Test Account 1',
            'Status': 'ACTIVE'
        }

        response: dict = bp.create(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)

    def test_brmobject_create(self):
        """Test create functionality with raw brmObject structure."""
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        payload: dict = {
            'brmObjects': {
                'Name': 'Test Account 2',
                'Status': 'ACTIVE'
            }
        }

        response: dict = bp.create(entity='ACCOUNT', data=payload)

        self.assertIsInstance(response, dict)


if __name__ == '__main__':
    unittest.main()
