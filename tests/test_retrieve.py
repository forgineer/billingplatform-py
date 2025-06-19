import logging
import requests
import unittest

from billingplatform import BillingPlatform


def get_credentials(path='credentials.json') -> dict:
    """
    Load credentials from a JSON file.
    """
    import json
    
    with open(path) as f:
        return json.load(f)


class TestBillingPlatformRetrieve(unittest.TestCase):
    def test_retrieve_by_id(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        data: dict = bp.retrieve_by_id("ACCOUNT", record_id=10)
        #print(data)

        self.assertIsInstance(data, dict)
    
    def test_retrieve_with_query(self):
        logging.basicConfig(level=logging.DEBUG)

        session_credentials = get_credentials()
        bp = BillingPlatform(**session_credentials)

        self.assertIsInstance(bp, BillingPlatform)
        self.assertIsInstance(bp.session, requests.Session)

        data: dict = bp.retrieve_by_query("ACCOUNT", queryAnsiSql="Id > 0")
        #print(data)

        self.assertIsInstance(data, dict)


if __name__ == '__main__':
    unittest.main()
