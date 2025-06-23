import logging
import requests
import unittest

from billingplatform import BillingPlatform
from billingplatform.api import BillingPlatformException
from utils_for_testing import get_credentials


class TestBillingPlatformQuery(unittest.TestCase):
    def test_basic_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        response: dict = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1")
        #print(response)

        self.assertIsInstance(response, dict)

    def test_query_exception(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)
        self.assertRaises(BillingPlatformException, bp.query, "SELECT Id WHERE 1=1")


if __name__ == '__main__':
    unittest.main()
