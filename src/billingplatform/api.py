import atexit
import logging
import requests

from . import exceptions
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

        # Construct base URLs
        self.auth_base_url: str = f'{self.base_url}/auth/{self.auth_api_version}'
        self.rest_base_url: str = f'{self.base_url}/rest/{self.rest_api_version}'


        if all([username, password]):
            self.login()
        elif all([client_id, client_secret, token_type]):
            self.oauth_login()
        else:
            raise ValueError("Either username/password or client_id/client_secret must be provided.")


    def _response_handler(self, response: requests.Response) -> dict:
        """
        Handle the response from the BillingPlatform API.

        :param response: The response object from the requests library.
        :return: The response data as a dictionary.
        :raises BillingPlatformException: If the response status code is not 200.
        """
        if response.status_code == 200:
            logging.debug(f'Success Response: {response.text}')
            return response.json()
        elif response.status_code == 400:
            raise exceptions.BillingPlatform400Exception(response)
        elif response.status_code == 401:
            raise exceptions.BillingPlatform401Exception(response)
        elif response.status_code == 404:
            raise exceptions.BillingPlatform404Exception(response)
        elif response.status_code == 429:
            raise exceptions.BillingPlatform429Exception(response)
        elif response.status_code == 500:
            raise exceptions.BillingPlatform500Exception(response)
        else:
            raise exceptions.BillingPlatformException(response)


    def login(self) -> None:
        """
        Authenticate with the BillingPlatform API using username and password.

        :return: None
        """
        if self.logout_at_exit:
            atexit.register(self.logout)
        else:
            logging.warning('Automatic logout at exit has been disabled. You must call logout() manually to close the session.')
        
        _login_url: str = f'{self.rest_base_url}/login'
        
        # Update session headers
        _login_payload: dict = {
            'username': self.username,
            'password': self.password,
        }

        try:
            _login_response: dict = self._response_handler(
                self.session.post(_login_url, json=_login_payload, **self.requests_parameters)
            )

            # Retrieve 'loginResponse' data
            _login_response_data: list[dict] = _login_response.get('loginResponse')

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
        raise NotImplementedError("OAuth login functionality is not implemented yet.")


    def logout(self) -> None:
        """
        Log out of the BillingPlatform API.

        :return: None
        """
        try:
            if self.session.headers.get('sessionid'):
                _logout_url: str = f'{self.rest_base_url}/logout'

                _logout_response: dict = self._response_handler(
                    self.session.post(_logout_url, **self.requests_parameters)
                )

                # If the logout is successful, we don't need to do anything further except close the session.

            # Close the session
            self.session.close()
        except requests.RequestException as e:
            raise Exception(f"Failed to logout: {e}")


    def query(self, sql: str) -> dict:
        """
        Execute a SQL query against the BillingPlatform API.

        :param sql: The SQL query to execute.
        :return: The query response data.
        """
        _url_encoded_sql: str = quote(sql)
        _query_url: str = f'{self.rest_base_url}/query?sql={_url_encoded_sql}'

        logging.debug(f'Query URL: {_query_url}')

        try:
            _query_response: dict = self._response_handler(
                self.session.get(_query_url, **self.requests_parameters)
            )

            return _query_response
        except requests.RequestException as e:
            raise Exception(f'Failed to execute query: {e}')


    def retrieve_by_id(self, 
                       entity: str, 
                       record_id: int) -> dict:
        """
        Retrieve an individual record from the BillingPlatform API.
        
        :param entity: The entity to retrieve records from.
        :param record_id: The 'Id' of the record to retrieve.
        :return: The retrieve response data.
        """
        _retrieve_url: str = f'{self.rest_base_url}/{entity}/{record_id}'
        
        logging.debug(f'Retrieve URL: {_retrieve_url}')

        try:
            _retrieve_response: dict = self._response_handler(
                self.session.get(_retrieve_url, **self.requests_parameters)
            )

            return _retrieve_response
        except requests.RequestException as e:
            raise Exception(f'Failed to retrieve records: {e}')


    def retrieve_by_query(self, 
                          entity: str, 
                          queryAnsiSql: str) -> dict:
        """
        Retrieve whole records from the BillingPlatform API with a query.
        
        :param entity: The entity to retrieve records from.
        :param queryAnsiSql: Optional ANSI SQL query to filter records.
        :return: The retrieve response data.
        """
        _url_encoded_sql: str = quote(queryAnsiSql)
        _retrieve_url: str = f'{self.rest_base_url}/{entity}?queryAnsiSql={_url_encoded_sql}'
        
        logging.debug(f'Retrieve URL: {_retrieve_url}')

        try:
            _retrieve_response: dict = self._response_handler(
                self.session.get(_retrieve_url, **self.requests_parameters)
            )

            return _retrieve_response
        except requests.RequestException as e:
            raise Exception(f'Failed to retrieve records: {e}')


    # Post
    def create(self, 
               entity: str, 
               data: list[dict] | dict) -> dict:
        """        
        Create records in BillingPlatform.

        :param entity: The entity to create a record for.
        :param data: The data to create the record with.
        :return: The create response data.
        """
        _create_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Create URL: {_create_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original

        if not isinstance(_data, dict) or 'brmObjects' not in _data:
            _data = {
                'brmObjects': data
            }

        logging.debug(f'Create data payload: {_data}')

        try:
            _create_response: dict = self._response_handler(
                self.session.post(_create_url, json=_data, **self.requests_parameters)
            )

            return _create_response
        except requests.RequestException as e:
            raise Exception(f'Failed to create record: {e}')


    # Put
    def update(self, 
               entity: str, 
               data: list[dict] | dict) -> dict:
        """
        Update records in BillingPlatform.

        :param entity: The entity to update records for.
        :param data: The data to update the records with.
        :return: The update response data.
        """
        _update_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Update URL: {_update_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original

        if not isinstance(_data, dict) or 'brmObjects' not in _data:
            _data = {
                'brmObjects': data
            }

        logging.debug(f'Update data payload: {_data}')

        try:
            _update_response: requests.Response = self._response_handler(
                self.session.put(_update_url, json=_data, **self.requests_parameters)
            )

            return _update_response
        except requests.RequestException as e:
            raise Exception(f'Failed to update record: {e}')


    # Patch
    def upsert(self, 
               entity: str, 
               data: list[dict] | dict,
               externalIDFieldName: str) -> dict:
        """
        Upsert records in BillingPlatform.

        :param entity: The entity to upsert records for.
        :param data: The data to upsert the records with.
        :param externalIDFieldName: The name of the external ID field to use for upsert.
        :return: The upsert response data.
        """
        _upsert_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Upsert URL: {_upsert_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original

        if not isinstance(_data, dict) or 'brmObjects' not in _data:
            _data = {
                'brmObjects': data,
                'externalIDFieldName': externalIDFieldName
            }
        else:
            _data['externalIDFieldName'] = externalIDFieldName

        logging.debug(f'Upsert data payload: {_data}')

        try:
            _upsert_response: dict = self._response_handler(
                self.session.patch(_upsert_url, json=_data, **self.requests_parameters)
            )

            return _upsert_response
        except requests.RequestException as e:
            raise Exception(f'Failed to upsert record: {e}')


    # Delete
    def delete(self, 
               entity: str, 
               data: list[dict] | dict,
               EmptyRecycleBin: bool = False) -> dict:
        """
        Delete records from BillingPlatform.

        :param entity: The entity to delete a record from.
        :param data: The data to delete the record with.
        :param EmptyRecycleBin: Whether to permanently delete the record (default is False).
        :return: The delete response data.
        """
        _delete_url: str = f'{self.rest_base_url}/delete/{entity}'
        logging.debug(f'Delete URL: {_delete_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original
        _EmptyRecycleBin: str = '0' if not EmptyRecycleBin else '1'

        if not isinstance(_data, dict) or 'brmObjects' not in _data:
            _data = {
                'brmObjects': data,
                'EmptyRecycleBin': _EmptyRecycleBin
            }
        else:
            _data['EmptyRecycleBin'] = _EmptyRecycleBin

        logging.debug(f'Delete data payload: {_data}')

        try:
            _delete_response: dict = self._response_handler(
                self.session.delete(_delete_url, json=_data, **self.requests_parameters)
            )

            return _delete_response
        except requests.RequestException as e:
            raise Exception(f'Failed to delete records: {e}')


    def undelete(self, ):
        raise NotImplementedError("Undelete functionality is not implemented yet.")

    def bulk_request(self, ):
        raise NotImplementedError("Bulk request functionality is not implemented yet.")
    
    def bulk_retreive(self, ):
        raise NotImplementedError("Bulk retrieve functionality is not implemented yet.")

    def file_upload(self, file_path: str):
        raise NotImplementedError("File upload functionality is not implemented yet.")

    def file_download(self, file_id: str):
        raise NotImplementedError("File download functionality is not implemented yet.")
