import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


"""
Tests assume an existing credentials file in the root directory. For more information of the expected format, 
see the utils_for_testing.py file.
"""

class TestBillingPlatformBulkQueryRequest(unittest.TestCase):
    def test_basic_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        bulk_query_response: dict = bp.bulk_query_request(RequestName='TestQuery', 
                                                          RequestBody='SELECT Id, Name, Status FROM ACCOUNT WHERE 1 = 1')

        self.assertIsInstance(bulk_query_response, dict)


if __name__ == '__main__':
    unittest.main()
