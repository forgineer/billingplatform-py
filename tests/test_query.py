import logging
import pandas as pd
import unittest

from billingplatform import BillingPlatform


class TestBillingPlatformQuery(unittest.TestCase):
    def test_basic_query(self):
        logging.basicConfig(level=logging.DEBUG)

        # Fake credentials for testing against the mock server
        session_credentials = {
            'base_url': 'http://localhost',
            'username': 'blake',
            'password': 'passwd'
        }

        bp = BillingPlatform(**session_credentials)

        data: list[dict] = bp.query("SELECT * FROM ACCOUNTS WHERE 1=1")
        print(data)

        #data_df: pd.DataFrame = pd.DataFrame(data)
        #print(data_df)


if __name__ == '__main__':
    unittest.main()
