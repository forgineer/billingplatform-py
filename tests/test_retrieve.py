import logging
import pandas as pd
import unittest

from billingplatform import BillingPlatform


class TestBillingPlatformRetrieve(unittest.TestCase):
    def test_basic_retrieve(self):
        logging.basicConfig(level=logging.DEBUG)

        # Fake credentials for testing against the mock server
        session_credentials = {
            'base_url': 'http://localhost',
            'username': 'blake',
            'password': 'passwd'
        }

        bp = BillingPlatform(**session_credentials)

        data: list[dict] = bp.retrieve("ACCOUNT")
        print(data)

        #data_df: pd.DataFrame = pd.DataFrame(data)
        #print(data_df)

    def test_retrieve_by_id(self):
        logging.basicConfig(level=logging.DEBUG)

        # Fake credentials for testing against the mock server
        session_credentials = {
            'base_url': 'http://localhost',
            'username': 'blake',
            'password': 'passwd'
        }

        bp = BillingPlatform(**session_credentials)

        data: list[dict] = bp.retrieve("ACCOUNT", record_id=10)
        print(data)

        #data_df: pd.DataFrame = pd.DataFrame(data)
        #print(data_df)
    
    def test_retrieve_with_query(self):
        logging.basicConfig(level=logging.DEBUG)

        # Fake credentials for testing against the mock server
        session_credentials = {
            'base_url': 'http://localhost',
            'username': 'blake',
            'password': 'passwd'
        }

        bp = BillingPlatform(**session_credentials)

        data: list[dict] = bp.retrieve("ACCOUNT", queryAnsiSql="Id > 0")
        print(data)

        #data_df: pd.DataFrame = pd.DataFrame(data)
        #print(data_df)


if __name__ == '__main__':
    unittest.main()
