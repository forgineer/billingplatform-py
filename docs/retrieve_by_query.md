[← Back to Documentation Home](README.md)

# `BillingPlatform.retrieve_by_query`

Retrieve records from BillingPlatform using an ANSI SQL query filter.

## Syntax

```python
BillingPlatform.retrieve_by_query(entity: str, queryAnsiSql: str) -> dict
```

## Parameters

| Parameter      | Type   | Description                                                        |
|----------------|--------|--------------------------------------------------------------------|
| `entity`       | `str`  | The name of the entity to query (e.g., `"ACCOUNT"`).               |
| `queryAnsiSql` | `str`  | The ANSI SQL query string to filter records.                       |

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The main results are typically found under the `"retrieveResponse"` key. |

## Examples

### Basic Usage

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

response = bp.retrieve_by_query(entity="ACCOUNT", queryAnsiSql="Id > 0")
records = response.get("retrieveResponse", [])
for record in records:
    print(record)
```

## Notes

- The `entity` parameter should match the BillingPlatform object type you wish to query.
- The SQL syntax must be supported by BillingPlatform's API.

---

[← Back to Documentation Home](README.md)