import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


"""
Tests assume an existing credentials file in the root directory. For more information of the expected format, 
see the utils_for_testing.py file.
"""

class TestBillingPlatformRetrieve(unittest.TestCase):
    def test_retrieve_by_id(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        _record_id: int = 1  # Replace with a valid ID for your test, works with mock server data
        response: dict = bp.retrieve_by_id("ACCOUNT", record_id=_record_id)

        self.assertIsInstance(response, dict)
    
    def test_retrieve_with_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        _queryAnsiSql: str = "Id > 0"  # Replace with a valid query for your test, works with mock server data
        response: dict = bp.retrieve_by_query("ACCOUNT", queryAnsiSql=_queryAnsiSql)

        self.assertIsInstance(response, dict)


if __name__ == '__main__':
    unittest.main()
