import atexit
import logging
import requests

from .handlers import response_handler
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
        
        _login_url: str = f'{self.rest_base_url}/login'
        
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
        raise NotImplementedError("OAuth login functionality is not implemented yet.")


    def logout(self) -> None:
        """
        Log out of the BillingPlatform API.

        :return: None
        :raises Exception: If logout fails or response does not contain expected data.
        """
        try:
            if self.session.headers.get('sessionid'):
                _logout_url: str = f'{self.rest_base_url}/logout'
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
        _query_url: str = f'{self.rest_base_url}/query?sql={_url_encoded_sql}'

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
        Retrieve an individual record from the BillingPlatform API.
        
        :param entity: The entity to retrieve records from.
        :param record_id: The 'Id' of the record to retrieve.
        :return: The retrieve response data.
        :raises Exception: If retrieve fails or response does not contain expected data.
        """
        _retrieve_url: str = f'{self.rest_api_version}/{entity}/{record_id}'
        
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
        Retrieve whole records from the BillingPlatform API with a query.
        
        :param entity: The entity to retrieve records from.
        :param queryAnsiSql: Optional ANSI SQL query to filter records.
        :return: The retrieve response data.
        :raises Exception: If retrieve fails or response does not contain expected data.
        """
        _url_encoded_sql: str = quote(queryAnsiSql)
        _retrieve_url: str = f'{self.rest_api_version}/{entity}?queryAnsiSql={_url_encoded_sql}'
        
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
    def create(self, 
               entity: str, 
               data: list[dict] | dict) -> dict:
        """        
        Create records in BillingPlatform.

        :param entity: The entity to create a record for.
        :param data: The data to create the record with.
        :return: The create response data.
        :raises Exception: If create fails or response does not contain expected data.
        """
        _create_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Create URL: {_create_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original

        if not _data.get('brmObjects', False):
            _data = {
                'brmObjects': data
            }

        logging.debug(f'Create data payload: {_data}')

        try:
            _create_response: requests.Response = self.session.post(_create_url, json=_data, **self.requests_parameters)

            if _create_response.status_code != 200:
                raise response_handler(_create_response)
            else:
                logging.debug(f'Create successful: {_create_response.text}')
            
            # Retrieve 'createResponse' data
            _create_response_data: dict = _create_response.json()

            if not _create_response_data:
                raise Exception('Create response did not contain createResponse data.')

            return _create_response_data
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
        :raises Exception: If update fails or response does not contain expected data.
        """
        _update_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Update URL: {_update_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original

        if not data.get('brmObjects', False):
            _data = {
                'brmObjects': data
            }

        logging.debug(f'Update data payload: {_data}')

        try:
            _update_response: requests.Response = self.session.put(_update_url, json=_data, **self.requests_parameters)

            if _update_response.status_code != 200:
                raise response_handler(_update_response)
            else:
                logging.debug(f'Update successful: {_update_response.text}')
            
            # Retrieve 'updateResponse' data
            _update_response_data: dict = _update_response.json()

            if not _update_response_data:
                raise Exception('Update response did not contain updateResponse data.')

            return _update_response_data
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
        :raises Exception: If upsert fails or response does not contain expected data.
        """
        _upsert_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Upsert URL: {_upsert_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original

        if not data.get('brmObjects', False):
            _data = {
                'brmObjects': data,
                'externalIDFieldName': externalIDFieldName
            }
        else:
            _data['externalIDFieldName'] = externalIDFieldName

        logging.debug(f'Upsert data payload: {_data}')

        try:
            _upsert_response: requests.Response = self.session.patch(_upsert_url, json=_data, **self.requests_parameters)

            if _upsert_response.status_code != 200:
                raise response_handler(_upsert_response)
            else:
                logging.debug(f'Upsert successful: {_upsert_response.text}')
            
            # Retrieve 'upsertResponse' data
            _upsert_response_data: dict = _upsert_response.json()

            if not _upsert_response_data:
                raise Exception('Upsert response did not contain upsertResponse data.')

            return _upsert_response_data
        except requests.RequestException as e:
            raise Exception(f'Failed to upsert record: {e}')


    # Delete
    def delete(self, 
               entity: str, 
               data: list[dict] | dict) -> dict:
        """
        Delete records from BillingPlatform.

        :param entity: The entity to delete a record from.
        :param data: The data to delete the record with.
        :return: The delete response data.
        :raises Exception: If delete fails or response does not contain expected data.
        """
        _delete_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Delete URL: {_delete_url}')

        _data: dict = data.copy()  # Create a copy of the data to avoid modifying the original

        if not data.get('brmObjects', False):
            _data = {
                'brmObjects': data
            }

        logging.debug(f'Delete data payload: {_data}')

        try:
            _delete_response: requests.Response = self.session.delete(_delete_url, json=data, **self.requests_parameters)

            if _delete_response.status_code != 200:
                raise response_handler(_delete_response)
            else:
                logging.debug(f'Delete successful: {_delete_response.text}')
            
            # Retrieve 'deleteResponse' data
            _delete_response_data: dict = _delete_response.json()

            if not _delete_response_data:
                raise Exception('Delete response did not contain deleteResponse data.')

            return _delete_response_data
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
