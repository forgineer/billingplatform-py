import atexit
import logging
import requests

from urllib.parse import quote


AUTH_API_VERSION = '1.0'
REST_API_VERSION = '2.0'
LOGOUT_AT_EXIT = True


class BillingPlatform:
    def __init__(self, 
                 base_url: str,
                 username: str = None, 
                 password: str = None, 
                 client_id: str = None, 
                 client_secret: str = None,
                 token_type: str = 'access_token' # access_token or refresh_token
                ):
        """
        Initialize the BillingPlatform API client.
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()

        if all([username, password]):
            self.login()
        elif all([client_id, client_secret, token_type]):
            self.oauth_login()
        else:
            raise ValueError("Either username/password or client_id/client_secret must be provided.")


    def login(self) -> None:
        """
        Authenticate with the BillingPlatform API and return a session object with sesstion ID.
        """
        if LOGOUT_AT_EXIT:
            atexit.register(self.logout)
        
        _login_url: str = f'{self.base_url}/rest/{REST_API_VERSION}/login'
        
        # Update session headers
        _login_payload = {
            'username': self.username,
            'password': self.password,
        }

        try:
            _login_response = self.session.post(_login_url, json=_login_payload)

            if _login_response.status_code != 200:
                raise Exception(f'Login failed with status code: {_login_response.status_code}, response: {_login_response.text}')
            else:
                logging.debug(f'Login successful: {_login_response.text}')
            
            # Retrieve 'loginResponse' data
            _login_response_data = _login_response.json().get('loginResponse')

            if not _login_response_data:
                raise Exception('Login response did not contain loginResponse data.')

            # Update session headers with session ID
            _session_id: str = _login_response_data[0].get('SessionID')

            if _session_id:
                self.session.headers.update({'sessionid': _session_id})
            else:
                raise Exception('Login response did not contain a session ID.')
        except requests.RequestException as e:
            raise Exception(f'Failed to login: {e}')
    

    def oauth_login(self):
        """
        Authenticate with the BillingPlatform API using OAuth and return an access token.
        """
        ...


    def logout(self):
        """
        Log out of the BillingPlatform API.
        """
        try:
            if self.session.headers.get('sessionid'):
                _logout_url = f'{self.base_url}/rest/{REST_API_VERSION}/logout'
                _logout_response = self.session.post(_logout_url)

                if _logout_response.status_code != 200:
                    raise Exception(f'Logout failed with status code: {_logout_response.status_code}, response: {_logout_response.text}')
                else:
                    logging.debug(f'Logout successful: {_logout_response.text}')
            
            # Clear session
            self.session.close()
        except requests.RequestException as e:
            raise Exception(f"Failed to logout: {e}")


    def query(self, sql: str):
        """
        Execute a SQL query against the BillingPlatform API and return the results.
        """
        _url_encoded_sql = quote(sql)
        _query_url = f'{self.base_url}/rest/{REST_API_VERSION}/query?sql={_url_encoded_sql}'

        try:
            _query_response = self.session.get(_query_url)

            if _query_response.status_code != 200:
                raise Exception(f'Query failed with status code: {_query_response.status_code}, response: {_query_response.text}')
            else:
                logging.debug(f'Query successful: {_query_response.text}')
            
            # Retrieve 'queryResponse' data
            _query_response_data = _query_response.json().get('queryResponse')

            if not _query_response_data:
                raise Exception('Query response did not contain queryResponse data.')

            return _query_response_data
        except requests.RequestException as e:
            raise Exception(f'Failed to execute query: {e}')


    def retrieve(self, 
                 entity: str, 
                 record_id: int = None, 
                 queryAnsiSql: str = None):
        ...


    # Post
    def create(self, ):
        ...


    # Put
    def update(self, ):
        ...


    # Patch
    def upsert(self, ):
        ...


    # Delete
    def delete(self, ):
        ...


    def undelete(self, ):
        ...


    def file_upload(self, file_path: str):
        ...


    def file_download(self, file_id: str):
        ...
