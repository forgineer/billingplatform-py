import atexit
import logging
import requests

from .utils import response_handler
from urllib.parse import quote # for URL encoding


class BillingPlatform:
    def __init__(self, 
                 base_url: str,
                 username: str = None, 
                 password: str = None, 
                 client_id: str = None, 
                 client_secret: str = None,
                 token_type: str = 'access_token', # access_token or refresh_token
                 requests_parameters: dict = None,
                 auth_api_version: str = '1.0', # /auth endpoint
                 rest_api_version: str = '2.0', # /rest endpoint
                 logout_at_exit: bool = True
                ):
        """
        Initialize the BillingPlatform API client.

        :param base_url: The base URL of the BillingPlatform API.
        :param username: Username for authentication (optional if using OAuth).
        :param password: Password for authentication (optional if using OAuth).
        :param client_id: Client ID for OAuth authentication (optional if using username/password).
        :param client_secret: Client secret for OAuth authentication (optional if using username/password).
        :param token_type: Type of token to use for OAuth ('access_token' or 'refresh_token').
        :param requests_parameters: Additional parameters to pass to each request made by the client (optional).
        :param auth_api_version: Version of the authentication API (default is '1.0').
        :param rest_api_version: Version of the REST API (default is '2.0').
        :param logout_at_exit: Whether to log out automatically at exit (default is True).
        
        :raises ValueError: If neither username/password nor client_id/client_secret is provided.
        :raises BillingPlatformException: If login fails or response does not contain expected data.
        """
        self.base_url: str = base_url.rstrip('/')
        self.username: str = username
        self.password: str = password
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.requests_parameters: dict = requests_parameters or {}
        self.auth_api_version: str = auth_api_version
        self.rest_api_version: str = rest_api_version
        self.logout_at_exit: bool = logout_at_exit
        self.session: requests.Session = requests.Session()


        if all([username, password]):
            self.login()
        elif all([client_id, client_secret, token_type]):
            self.oauth_login()
        else:
            raise ValueError("Either username/password or client_id/client_secret must be provided.")


    def login(self) -> None:
        """
        Authenticate with the BillingPlatform API using username and password.

        :return: None
        :raises Exception: If login fails or response does not contain expected data.
        """
        if self.logout_at_exit:
            atexit.register(self.logout)
        else:
            logging.warning('Automatic logout at exit has been disabled. You must call logout() manually to close the session.')
        
        _login_url: str = f'{self.base_url}/rest/{self.rest_api_version}/login'
        
        # Update session headers
        _login_payload: dict = {
            'username': self.username,
            'password': self.password,
        }

        try:
            _login_response: requests.Response = self.session.post(_login_url, json=_login_payload, **self.requests_parameters)

            if _login_response.status_code != 200:
                raise response_handler(_login_response)
            else:
                logging.debug(f'Login successful: {_login_response.text}')
            
            # Retrieve 'loginResponse' data
            _login_response_data: list[dict] = _login_response.json().get('loginResponse')

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
    

    def oauth_login(self) -> None:
        """
        Authenticate with the BillingPlatform API using OAuth and return an access token.
        """
        ...


    def logout(self) -> None:
        """
        Log out of the BillingPlatform API.

        :return: None
        :raises Exception: If logout fails or response does not contain expected data.
        """
        try:
            if self.session.headers.get('sessionid'):
                _logout_url: str = f'{self.base_url}/rest/{self.rest_api_version}/logout'
                _logout_response: requests.Response = self.session.post(_logout_url, **self.requests_parameters)

                if _logout_response.status_code != 200:
                    raise response_handler(_logout_response)
                else:
                    logging.debug(f'Logout successful: {_logout_response.text}')
            
            # Clear session
            self.session.close()
        except requests.RequestException as e:
            raise Exception(f"Failed to logout: {e}")


    def query(self, sql: str) -> dict:
        """
        Execute a SQL query against the BillingPlatform API.

        :param sql: The SQL query to execute.
        :return: The query response data.
        :raises Exception: If query fails or response does not contain expected data.
        """
        _url_encoded_sql: str = quote(sql)
        _query_url: str = f'{self.base_url}/rest/{self.rest_api_version}/query?sql={_url_encoded_sql}'

        logging.debug(f'Query URL: {_query_url}')

        try:
            _query_response: requests.Response = self.session.get(_query_url, **self.requests_parameters)

            if _query_response.status_code != 200:
                raise response_handler(_query_response)
            else:
                logging.debug(f'Query successful: {_query_response.text}')
            
            # Retrieve 'queryResponse' data
            _query_response_data: dict = _query_response.json()

            if not _query_response_data:
                raise Exception('Query response did not contain queryResponse data.')

            return _query_response_data
        except requests.RequestException as e:
            raise Exception(f'Failed to execute query: {e}')


    def retrieve_by_id(self, 
                       entity: str, 
                       record_id: int) -> dict:
        """
        Retrieve records from the BillingPlatform API.
        
        :param entity: The entity to retrieve records from.
        :param record_id: The ID of the record to retrieve.
        :return: The retrieve response data.
        :raises Exception: If retrieve fails or response does not contain expected data.
        """
        _retrieve_url: str = f'{self.base_url}/rest/{self.rest_api_version}/{entity}/{record_id}'
        
        logging.debug(f'Retrieve URL: {_retrieve_url}')

        try:
            _retrieve_response: requests.Response = self.session.get(_retrieve_url, **self.requests_parameters)

            if _retrieve_response.status_code != 200:
                raise response_handler(_retrieve_response)
            else:
                logging.debug(f'Retrieve successful: {_retrieve_response.text}')
            
            # Retrieve 'retrieveResponse' data
            _retrieve_response_data: dict = _retrieve_response.json()

            if not _retrieve_response_data:
                raise Exception('Retrieve response did not contain retrieveResponse data.')

            return _retrieve_response_data
        except requests.RequestException as e:
            raise Exception(f'Failed to retrieve records: {e}')


    def retrieve_by_query(self, 
                          entity: str, 
                          queryAnsiSql: str) -> dict:
        """
        Retrieve records from the BillingPlatform API.
        
        :param entity: The entity to retrieve records from.
        :param queryAnsiSql: Optional ANSI SQL query to filter records.
        :return: The retrieve response data.
        :raises Exception: If retrieve fails or response does not contain expected data.
        """
        _url_encoded_sql: str = quote(queryAnsiSql)
        _retrieve_url: str = f'{self.base_url}/rest/{self.rest_api_version}/{entity}?queryAnsiSql={_url_encoded_sql}'
        
        logging.debug(f'Retrieve URL: {_retrieve_url}')

        try:
            _retrieve_response: requests.Response = self.session.get(_retrieve_url, **self.requests_parameters)

            if _retrieve_response.status_code != 200:
                raise response_handler(_retrieve_response)
            else:
                logging.debug(f'Retrieve successful: {_retrieve_response.text}')
            
            # Retrieve 'retrieveResponse' data
            _retrieve_response_data: dict = _retrieve_response.json()

            if not _retrieve_response_data:
                raise Exception('Retrieve response did not contain retrieveResponse data.')

            return _retrieve_response_data
        except requests.RequestException as e:
            raise Exception(f'Failed to retrieve records: {e}')


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
