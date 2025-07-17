# Documentation

Welcome to the documentation for the BillingPlatform Python library! This package provides a simple, robust interface for interacting with the BillingPlatform REST API, supporting authentication, querying, and record management.

## Getting Started

### Installation

Install the library using pip:

```sh
pip install billingplatform
```

### Authentication

You can authenticate with BillingPlatform using either a username/password or OAuth client credentials.

#### 1. Username and Password

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)
```

#### 2. OAuth Client Credentials

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    client_id="your_client_id",
    client_secret="your_client_secret",
    use_token="access_token"  # or "refresh_token"
)
```

> **Tip:** Never hardcode credentials in production code. Use environment variables or a secure credentials file.

---

## Next Steps

Once authenticated, you can use the following methods. See the linked documentation for details and examples:

- [Query Records](query.md)
- [Retrieve by ID](retrieve_by_id.md)
- [Retrieve by Query](retrieve_by_query.md)
- [Create Records](create.md)
- [Update Records](update.md)
- [Upsert Records](upsert.md)
- [Delete Records](delete.md)
- [Undelete Records](undelete.md)
- [Bulk Query Request](bulk_query_request.md)
- [Bulk Retrieve Request](bulk_retrieve_request.md)
- [Logout](logout.md)

---

## Example Usage

```python
# Example: Query active accounts
response = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE Status = 'ACTIVE'")
accounts = response.get("queryResponse", [])
for account in accounts:
    print(account)
```

## Converting API Responses to a DataFrame

You can easily convert BillingPlatform API responses to a DataFrame for additional transformation or analysis.  
Most responses contain a single key (such as `"queryResponse"` or `"retrieveResponse"`) with a list of records.

Here's an example with a reusable function where the data is extracting and converted to a pandas DataFrame:

```python
import pandas as pd

def response_to_dataframe(response: dict) -> pd.DataFrame:
    """
    Converts a BillingPlatform API response to a pandas DataFrame.
    Automatically detects the main response key.
    """
    # Find the first key with a list value
    for value in response.values():
        if isinstance(value, list):
            return pd.DataFrame(value)
    # If no list found, return empty DataFrame
    return pd.DataFrame()

# Usage example:
response = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE Status = 'ACTIVE'")
df = response_to_dataframe(response)
print(df)
```

---

For more details, see the [API source code](../src/billingplatform/api.py) or browse the [tests](../tests/README.md) for practical examples.