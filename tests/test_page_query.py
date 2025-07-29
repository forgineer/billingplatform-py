import logging
import requests
import unittest

from billingplatform import BillingPlatform
from utils_for_testing import get_credentials


"""
Tests assume an existing credentials file in the root directory. For more information of the expected format, 
see the utils_for_testing.py file.
"""

class TestBillingPlatformPageQuery(unittest.TestCase):
    def test_page_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        _page_size: int = 10
        for page in bp.page_query("SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1", page_size=_page_size):
            # Assert that that each page is a dictionary
            self.assertIsInstance(page, dict)

            # Assert that the data returned is equal to or less than the page size
            data = page.get('queryResponse', [])
            self.assertTrue(len(data) <= _page_size)

    def test_page_query_offset(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials('credentials.json', 'login')
        bp: BillingPlatform = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        _page_size: int = 10
        _offset: int = 1
        for page in bp.page_query("SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1", page_size=_page_size, offset=_offset):
            # Assert that that each page is a dictionary
            self.assertIsInstance(page, dict)
            # TODO: Add assertions to check the offset functionality


if __name__ == '__main__':
    unittest.main()
