import atexit
import base64
import logging
import requests

from . import exceptions
from typing import Iterator, Literal
from urllib.parse import quote # for URL encoding


class BillingPlatform:
    def __init__(self, 
                 base_url: str,
                 username: str | None = None, 
                 password: str | None = None, 
                 client_id: str | None = None, 
                 client_secret: str | None = None,
                 use_token: Literal['access_token', 'refresh_token'] = 'access_token',
                 requests_parameters: dict | None = None,
                 auth_api_version: str = '1.0', # /auth endpoint version
                 rest_api_version: str = '2.0', # /rest endpoint version
                 logout_at_exit: bool = True
                ):
        """
        Initialize the BillingPlatform API client.

        :param base_url: The base URL of the BillingPlatform API (ex. https://sandbox.billingplatform.com/myorg).
        :param username: Username for authentication (optional if using OAuth).
        :param password: Password for authentication (optional if using OAuth).
        :param client_id: Client ID for OAuth authentication (optional if using username/password).
        :param client_secret: Client secret for OAuth authentication (optional if using username/password).
        :param use_token: Type of token to use for OAuth ('access_token' or 'refresh_token').
        :param requests_parameters: Additional parameters to pass to each request made by the client (optional).
        :param auth_api_version: Version of the authentication API (default is '1.0').
        :param rest_api_version: Version of the REST API (default is '2.0').
        :param logout_at_exit: Whether to log out of the session automatically at exit (default is True).        
        :raises ValueError: If neither username/password nor client_id/client_secret is provided.
        :raises BillingPlatformException: If login fails or response does not contain expected data.
        """
        self.base_url: str = base_url.rstrip('/')
        self.username: str | None = username
        self.password: str | None = password
        self.client_id: str | None = client_id
        self.client_secret: str | None = client_secret
        self.use_token: str | None = use_token
        self.token: str | None = None
        self.requests_parameters: dict = requests_parameters or {}
        self.auth_api_version: str = auth_api_version
        self.rest_api_version: str = rest_api_version
        self.logout_at_exit: bool = logout_at_exit
        self.session: requests.Session = requests.Session()

        # Construct base URLs
        self.auth_base_url: str = f'{self.base_url}/auth/{self.auth_api_version}'
        self.rest_base_url: str = f'{self.base_url}/rest/{self.rest_api_version}'


         # Authenticate based on provided credentials
        if all([self.username, self.password]):
            self._login()
        elif all([self.client_id, self.client_secret, self.use_token]):
            self._oauth_login()
        else:
            raise ValueError("Either username/password or client_id/client_secret must be provided.")


    def _response_handler(self, response: requests.Response) -> dict:
        """
        Handle the response from the BillingPlatform API.

        :param response: The response object returned from the request.
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


    def _login(self) -> None:
        """
        Authenticate with the BillingPlatform API using username and password. If successful, updates the session headers with the session ID.

        :return: None
        :raises Exception: If the login response does not contain a session ID.
        """
        if self.logout_at_exit:
            atexit.register(self.logout)
        else:
            logging.warning('Automatic logout at exit has been disabled. You must call logout() manually to close the session.')
        
        _login_url: str = f'{self.rest_base_url}/login'
        logging.debug(f'Login URL: {_login_url}')
        
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
    

    def _oauth_login(self) -> None:
        """
        Authenticate with the BillingPlatform API using OAuth and return an access and/or refresh token. if successful, updates the session headers with the authorization token.

        :return: None
        :raises BillingPlatformException: If the OAuth response does not contain the expected token.
        :raises Exception: If the authentication request fails.
        """
        _authenticate_url: str = f'{self.auth_base_url}/authenticate?grant_type=client_credentials'
        logging.debug(f'Authenticate URL: {_authenticate_url}')

        # Encode client credentials into base64
        _base64_credentials: str = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode('utf-8')).decode('utf-8')

        self.session.headers.update({'Authorization': f'Basic {_base64_credentials}'})

        try:
            _oauth_response: requests.Response = self._response_handler(
                self.session.post(_authenticate_url, **self.requests_parameters)
            )

            # Update session headers with the token
            if self.use_token in _oauth_response:
                self.token = _oauth_response[self.use_token]
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            else:
                raise exceptions.BillingPlatformException(f'OAuth response did not contain {self.use_token}. Ensure BillingPlatform is configured correctly to accept OAuth.')
        except requests.RequestException as e:
            raise Exception(f'Failed to authenticate with OAuth: {e}')


    def logout(self) -> None:
        """
        Log out of the BillingPlatform session. This should be called to close the session and clean up resources.

        :return: None
        :raises Exception: If the logout request fails.
        """
        try:
            if self.session.headers.get('sessionid', False):
                _logout_url: str = f'{self.rest_base_url}/logout'
                logging.debug(f'Logout URL: {_logout_url}')

                _logout_response: dict = self._response_handler(
                    self.session.post(_logout_url, **self.requests_parameters)
                )
                # If the logout is successful, we don't need to do anything further except close the session.
            else:
                logging.warning('No session ID found. Skipping logout.')

            # Close the session
            self.session.close()
        except requests.RequestException as e:
            raise Exception(f"Failed to logout: {e}")


    def query(self, 
              sql: str,
              offset: int = 0,
              limit: int = 0) -> dict:
        """
        Execute a SQL query against the BillingPlatform API.

        :param sql: The SQL query to execute. It should be a valid SQL statement that the BillingPlatform API can process.
        :param offset: The number of rows to skip before starting to return rows (default is 0).
        :param limit: The maximum number of rows to return (default is 0, which means no limit).
        :return: The query response data.
        :raises Exception: If the query request fails.
        """
        # Encode the SQL query for URL
        _url_encoded_sql: str = ''

        if 'OFFSET' in sql.upper() or 'LIMIT' in sql.upper():
            _url_encoded_sql = quote(sql)
        else:
            if offset:
                sql = f'{sql} OFFSET {offset} ROWS'
            
            if limit:
                sql = f'{sql} FETCH NEXT {limit} ROWS ONLY'
            
            _url_encoded_sql = quote(sql)

        _query_url: str = f'{self.rest_base_url}/query?sql={_url_encoded_sql}'
        logging.debug(f'Query URL: {_query_url}')

        try:
            _query_response: dict = self._response_handler(
                self.session.get(_query_url, **self.requests_parameters)
            )

            return _query_response
        except requests.RequestException as e:
            raise Exception(f'Failed to execute query: {e}')
    

    def page_query(self, 
                   sql: str,
                   page_size: int = 1000,
                   offset: int = 0) -> Iterator[dict]:
        """
        Execute a paginated SQL query against the BillingPlatform API (as a generator).
        Yields each page of results as a dict.
        
        :param sql: The SQL query to execute. It should be a valid SQL statement that the BillingPlatform API can process.
        :param page_size: The number of rows to return per page (default is 1000).
        :param offset: The number of rows to skip before starting to return rows (default is 0).
        :return: A generator that yields query response data for each page.
        :raises Exception: If the query request fails.
        """
        _offset: int = offset

        if page_size > 10000:
            logging.warning('BillingPlatform API has a limit of 10,000 records per page. Setting page_size to 10,000.')
        _limit: int = min(page_size, 10000)

        while True:
            try:
                _query_response: dict = self.query(sql, offset=_offset, limit=_limit)
                yield _query_response
                _offset += _limit
            except exceptions.BillingPlatform404Exception:
                break  # No more records to fetch
            except requests.RequestException as e:
                raise Exception(f'Failed to execute paginated query: {e}')


    def retrieve_by_id(self, 
                       entity: str, 
                       record_id: int) -> dict:
        """
        Retrieve an individual record from the BillingPlatform API.
        
        :param entity: The entity to retrieve records from.
        :param record_id: The 'Id' of the record to retrieve.
        :return: The retrieve response data.
        :raises Exception: If the retrieve request fails.
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
        :raises Exception: If the retrieve request fails.
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
        Create records in BillingPlatform. Please review the BillingPlatform API documentation for limits on the number of records that can be created in a single request.

        :param entity: The entity to create a record for.
        :param data: The data to create the record with.
        :return: The create response data. This will contain the ID of the newly created record(s).
        :raises Exception: If the create request fails.
        """
        _create_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Create URL: {_create_url}')

        _data: dict = data.copy() 

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
        :return: The update response data. This will contain the ID of the updated record(s) or error messages upon failure.
        :raises Exception: If the update request fails.
        """
        _update_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Update URL: {_update_url}')

        _data: dict = data.copy()

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
        Upsert records in BillingPlatform. If the record exists, it will be updated; if not, it will be created.

        :param entity: The entity to upsert records for.
        :param data: The data to upsert the records with.
        :param externalIDFieldName: The name of the external ID field to use for upsert.
        :return: The upsert response data.
        :raises Exception: If the upsert request fails.
        """
        _upsert_url: str = f'{self.rest_base_url}/{entity}'
        logging.debug(f'Upsert URL: {_upsert_url}')

        _data: dict = data.copy()

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
        :param data: The data to delete the record with. This should only contain the IDs of the records to be deleted.
        :param EmptyRecycleBin: Whether to permanently delete the record (default is False).
        :return: The delete response data.
        :raises Exception: If the delete request fails.
        """
        _delete_url: str = f'{self.rest_base_url}/delete/{entity}'
        logging.debug(f'Delete URL: {_delete_url}')

        _data: dict = data.copy()
        _EmptyRecycleBin: str = '0' if not EmptyRecycleBin else '1'

        if not isinstance(_data, dict) or 'brmObjects' not in _data:
            _data = {
                'brmObjects': data,
                'EmptyRecycleBin': _EmptyRecycleBin
            }
        else:
            if 'EmptyRecycleBin' not in _data:
                _data['EmptyRecycleBin'] = _EmptyRecycleBin

        logging.debug(f'Delete data payload: {_data}')

        try:
            _delete_response: dict = self._response_handler(
                self.session.delete(_delete_url, json=_data, **self.requests_parameters)
            )

            return _delete_response
        except requests.RequestException as e:
            raise Exception(f'Failed to delete records: {e}')


    def undelete(self, 
                 entity: str, 
                 data: list[dict] | dict) -> dict:
        """
        Undelete records from the recycle bin in BillingPlatform.

        :param entity: The entity to undelete records for.
        :param data: The data to undelete the records with. This should only contain the IDs of the records to be undeleted.
        :return: The undelete response data.
        :raises Exception: If the undelete request fails.
        """
        _undelete_url: str = f'{self.rest_base_url}/undelete/{entity}'
        logging.debug(f'Undelete URL: {_undelete_url}')

        _data: dict = data.copy()

        if not isinstance(_data, dict) or 'brmObjects' not in _data:
            _data = {
                'brmObjects': data
            }

        logging.debug(f'Undelete data payload: {_data}')

        try:
            _undelete_response: dict = self._response_handler(
                self.session.delete(_undelete_url, json=_data, **self.requests_parameters)
            )

            return _undelete_response
        except requests.RequestException as e:
            raise Exception(f'Failed to undelete records: {e}')
        

    def bulk_query_request(self,
                           RequestName: str,
                           RequestBody: str,
                           RequestsPerBatch: int = 10000,
                           ResponseFormat: Literal['CSV', 'JSON'] = "JSON") -> dict:
        """
        Make a bulk query request to the BillingPlatform API. The request will be processed asynchronously, and you can check the status 
        of the request within the BillingPlatform UI.

        :param RequestName: Descriptive name of the new request.
        :param RequestBody: The request payload created using the BillingPlatform Query Language. The payload length cannot exceed 4000 characters.
        :param RequestsPerBatch: Number of records returned in one batch (default is 10000).
        :param ResponseFormat: The format of the response (default is 'JSON').
        :return: A response containing the ID of the request being processed.
        :raises Exception: If the query request fails.
        """
        _bulk_query_url: str = f'{self.rest_base_url}/bulk_api_request'
        logging.debug(f'Bulk query request URL: {_bulk_query_url}')

        _data: dict = {
            'brmObjects': {
                'RequestName': RequestName,
                'RequestBody': RequestBody,
                'RequestsPerBatch': RequestsPerBatch,
                'ResponseFormat': ResponseFormat,
                'RequestMethod': 'QUERY'  # Default to QUERY method
            }
        }

        logging.debug(f'Bulk query request payload: {_data}')

        try:
            _bulk_query_response: dict = self._response_handler(
                self.session.post(_bulk_query_url, json=_data, **self.requests_parameters)
            )

            return _bulk_query_response
        except requests.RequestException as e:
            raise Exception(f'Failed to post bulk query request: {e}')


    def bulk_retrieve_request(self, 
                              RequestName: str,
                              RequestBody: str,
                              RetrieveEntityName: str,
                              Columns: list[str] | None = None,
                              RequestsPerBatch: int = 10000,
                              CSVDelimiter: str = ',',
                              CSVQualifier: str = '\"',
                              CSVEndLineFormat: Literal['CR', 'LF', 'CRLF'] = "CRLF") -> dict:
        """
        Perform a bulk retrieve request to the BillingPlatform API. The request will be processed asynchronously, and you can check the status 
        of the request within the BillingPlatform UI.

        :param RequestName: Descriptive name of the new request.
        :param RequestBody: The request payload created using a standard ANSI SQL query.
        :param RetrieveEntityName: The name of the entity to retrieve records from.
        :param Columns: Optional list of columns to retrieve. If None, all columns are retrieved.
        :param RequestsPerBatch: Number of records returned in one batch (default is 10000).
        :param CSVDelimiter: Delimiter for CSV format (default is ',').
        :param CSVQualifier: Qualifier for CSV format (default is '\"').
        :param CSVEndLineFormat: End line format for CSV (default is 'CRLF').
        :return: A response containing the ID of the request being processed.
        :raises Exception: If the retrieve request fails.
        """
        _bulk_query_url: str = f'{self.rest_base_url}/bulk_api_request'
        logging.debug(f'Bulk retrieve request URL: {_bulk_query_url}')

        _data: dict = {
            'brmObjects': {
                'RequestName': RequestName,
                'RequestBody': RequestBody,
                'RequestsPerBatch': RequestsPerBatch,
                'RetrieveEntityName': RetrieveEntityName,
                'Columns': Columns if Columns is not None else [],
                'CSVDelimiter': CSVDelimiter,
                'CSVQualifier': CSVQualifier,
                'CSVEndLineFormat': CSVEndLineFormat,
                'RequestMethod': 'RETRIEVE',  # Default to RETRIEVE method
                'ResponseFormat': 'CSV'  # Default response format
            }
        }

        logging.debug(f'Bulk retrieve request payload: {_data}')

        try:
            _bulk_retrieve_response: dict = self._response_handler(
                self.session.post(_bulk_query_url, json=_data, **self.requests_parameters)
            )

            return _bulk_retrieve_response
        except requests.RequestException as e:
            raise Exception(f'Failed to post bulk retrieve request: {e}')
