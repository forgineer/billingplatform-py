# BillingPlatform API Client

This module provides the `BillingPlatform` class, a Python client for interacting with the BillingPlatform REST API. It supports authentication, querying, and CRUD operations.

## Class: `BillingPlatform`

### Initialization

```python
BillingPlatform(
    base_url: str,
    username: str = None,
    password: str = None,
    client_id: str = None,
    client_secret: str = None,
    token_type: str = 'access_token',
    requests_parameters: dict = None,
    auth_api_version: str = '1.0',
    rest_api_version: str = '2.0',
    logout_at_exit: bool = True
)
```

- **base_url**: Base URL of the BillingPlatform API.
- **username/password**: Credentials for session authentication.
- **client_id/client_secret/token_type**: Credentials for OAuth authentication (not yet implemented).
- **requests_parameters**: Additional parameters for each request (e.g., proxies, timeouts).
- **auth_api_version/rest_api_version**: API versioning.
- **logout_at_exit**: If `True`, logs out automatically on exit.

Raises `ValueError` if neither authentication method is provided.

---

### Methods

#### `login()`
Authenticate using username and password. Registers automatic logout if enabled.

#### `oauth_login()`
Authenticate using OAuth. *(Not implemented yet.)*

#### `logout()`
Logs out of the API and closes the session.

#### `query(sql: str) -> dict`
Executes a SQL query against the API.

- **sql**: SQL query string.
- **Returns**: Query response data.

#### `retrieve_by_id(entity: str, record_id: int) -> dict`
Retrieves a single record by entity and ID.

- **entity**: Entity name (e.g., "ACCOUNT").
- **record_id**: Record ID.

#### `retrieve_by_query(entity: str, queryAnsiSql: str) -> dict`
Retrieves records using an ANSI SQL query.

- **entity**: Entity name.
- **queryAnsiSql**: SQL filter.

#### `create(entity: str, data: list[dict] | dict) -> dict`
Creates new records.

- **entity**: Entity name.
- **data**: Record data (dict or list of dicts).

#### `update(entity: str, data: list[dict] | dict) -> dict`
Updates existing records.

- **entity**: Entity name.
- **data**: Record data.

#### `upsert(entity: str, data: list[dict] | dict, externalIDFieldName: str) -> dict`
Creates or updates records based on an external ID.

- **entity**: Entity name.
- **data**: Record data.
- **externalIDFieldName**: Field name for upsert matching.

#### `delete(entity: str, data: list[dict] | dict) -> dict`
Deletes records.

- **entity**: Entity name.
- **data**: Record data.

#### Not Implemented
- `undelete()`
- `bulk_request()`
- `bulk_retreive()`
- `file_upload(file_path: str)`
- `file_download(file_id: str)`

---

## Error Handling

All non-200 responses are handled by [`response_handler`](src/billingplatform/handlers.py), which raises custom exceptions defined in [`exceptions.py`](src/billingplatform/exceptions.py):

- `BillingPlatform400Exception`
- `BillingPlatform401Exception`
- `BillingPlatform404Exception`
- `BillingPlatform429Exception`
- `BillingPlatform500Exception`
- `BillingPlatformException` (generic)

---

## Example Usage

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(base_url="https://sandbox.billingplatform.com/myorg", username="myuser", password="mypassword")
response = bp.query("SELECT Id, Name FROM ACCOUNT WHERE Status = 'ACTIVE'")
print(response)
```

---

For more details, see the [source code](../src/billingplatform/api.py).