import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


class TestBillingPlatformRetrieve(unittest.TestCase):
    def test_retrieve_by_id(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        response: dict = bp.retrieve_by_id("ACCOUNT", record_id=10)
        #print(response)

        self.assertIsInstance(response, dict)
    
    def test_retrieve_with_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        response: dict = bp.retrieve_by_query("ACCOUNT", queryAnsiSql="Id > 0")
        #print(response)

        self.assertIsInstance(response, dict)


if __name__ == '__main__':
    unittest.main()
