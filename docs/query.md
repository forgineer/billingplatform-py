[← Back to Documentation Home](README.md)

# `BillingPlatform.query`

Query records from BillingPlatform using an ANSI SQL statement.

## Syntax

```python
BillingPlatform.query(
    sql: str,
    offset: int = 0,
    limit: int = 0
) -> dict
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sql`     | `str` | The ANSI SQL query string to execute against the BillingPlatform API. |
| `offset`  | `int` | (Optional) The number of rows to skip before starting to return rows. If not specified, no offset is applied. |
| `limit`   | `int` | (Optional) The maximum number of rows to return. If not specified, all matching rows are returned. |

> **Note:** If your SQL query already includes `OFFSET` or `LIMIT` clauses, the `offset` and `limit` parameters will be ignored.

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The main results are typically found under the `"queryResponse"` key. |

## Examples

### Basic Usage

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

response = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE Status = 'ACTIVE'")
accounts = response.get("queryResponse", [])
for account in accounts:
    print(account)
```

### Filtering Results

```python
sql = "SELECT Id, Name FROM ACCOUNT WHERE Status = 'ACTIVE'"
response = bp.query(sql)
active_accounts = response.get("queryResponse", [])
```

### Using Offset and Limit

```python
# Get the first 10 records
response = bp.query(
    "SELECT Id, Name FROM ACCOUNT WHERE Status = 'ACTIVE'",
    offset=0,
    limit=10
)
first_page = response.get("queryResponse", [])

# Get the next 10 records
response = bp.query(
    "SELECT Id, Name FROM ACCOUNT WHERE Status = 'ACTIVE'",
    offset=10,
    limit=10
)
second_page = response.get("queryResponse", [])
```

## Notes

- The SQL syntax must be supported by BillingPlatform's API. Refer to the official BillingPlatform documentation for supported SQL features.
- The `offset` and `limit` parameters are provided for convenience and will automatically append the correct BillingPlatform SQL pagination syntax if not already present.
- **For large data sets:** BillingPlatform enforces a 10,000 record limit per query. For easier paging through large result sets, use the [`page_query`](page_query.md) method, which automatically handles pagination for you.

---

[← Back to Documentation Home](README.md)