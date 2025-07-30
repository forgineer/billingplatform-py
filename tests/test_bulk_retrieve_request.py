import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


"""
Tests assume an existing credentials file in the root directory. For more information of the expected format, 
see the utils_for_testing.py file.
"""

class TestBillingPlatformBulkRetrieveRequest(unittest.TestCase):
    def test_basic_retrieve(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        bulk_request_response: dict = bp.bulk_retrieve_request(RequestName='TestRetrieve', 
                                                               RequestBody='Id > 0', 
                                                               RetrieveEntityName='ACCOUNT')   

        self.assertIsInstance(bulk_request_response, dict)


if __name__ == '__main__':
    unittest.main()
