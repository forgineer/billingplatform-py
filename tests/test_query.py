import logging
import requests
import unittest

from billingplatform import BillingPlatform
from billingplatform.exceptions import BillingPlatformException
from utils_for_testing import get_credentials


"""
Tests assume an existing credentials file in the root directory. For more information of the expected format, 
see the utils_for_testing.py file.
"""

class TestBillingPlatformQuery(unittest.TestCase):
    def test_basic_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        response: dict = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1")

        self.assertIsInstance(response, dict)

    def test_query_offset(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        _offset: int = 1
        response: dict = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1", offset=_offset)

        self.assertIsInstance(response, dict)
        # TODO: Add assertions to check the offset functionality

    def test_query_limit(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        _limit: int = 1
        response: dict = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1", limit=_limit)

        self.assertIsInstance(response, dict)
        self.assertLessEqual(len(response.get('records', [])), _limit)

    def test_query_exception(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)
        self.assertRaises(BillingPlatformException, bp.query, "SELECT Id WHERE 1=1")


if __name__ == '__main__':
    unittest.main()
