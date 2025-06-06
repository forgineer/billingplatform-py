import atexit
import requests


LOGOUT_AT_EXIT = False


class BillingPlatform:
    def __init__(self, client_id: str, client_secret: str, base_url: str = "https://api.billingplatform.com"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url

    def login(self):
        ...
    
    def logout(self):
        ...

    def query(self, sql: str):
        data = {
            "queryResponse": [
                {
                    "Id": 1,
                    "Name": "Account 1",
                    "Description": "The first account",
                    "Status": "ACTIVE"
                },
                {
                    "Id": 2,
                    "Name": "Account 2",
                    "Description": "The second account",
                    "Status": "ACTIVE"
                },
                {
                    "Id": 3,
                    "Name": "Account 3",
                    "Description": "The third account",
                    "Status": "INACTIVE"
                }
            ]
        }

        return data

    def create(self):
        ...

    def update(self, ):
        ...

    def upsert(self, ):
        ...

    def delete(self, ):
        ...

    if LOGOUT_AT_EXIT:
        atexit.register(logout)
