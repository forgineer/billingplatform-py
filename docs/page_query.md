[← Back to Documentation Home](README.md)

# `BillingPlatform.page_query`

Iterate through large query results from BillingPlatform using automatic pagination.

## Syntax

```python
BillingPlatform.page_query(
    sql: str,
    page_size: int = 1000,
    offset: int = 0
) -> Iterator[dict]
```

## Parameters

| Parameter   | Type   | Description |
|-------------|--------|-------------|
| `sql`       | `str`  | The ANSI SQL query string to execute against the BillingPlatform API. |
| `page_size` | `int`  | (Optional) The number of rows to return per page (default is 1000, max is 10,000). |
| `offset`    | `int`  | (Optional) The number of rows to skip before starting to return rows (default is 0). |

> **Note:** If your SQL query already includes `OFFSET` or `LIMIT` clauses, pagination may not work as expected.

## Returns

| Type           | Description |
|----------------|-------------|
| `Iterator[dict]` | A generator that yields each page of query response data as a dictionary. Each page contains a `"queryResponse"` key with a list of records. |

## Examples

### Iterating Through All Records

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

for page in bp.page_query("SELECT Id, Name FROM ACCOUNT WHERE Status = 'ACTIVE'", page_size=5000):
    records = page.get("queryResponse", [])
    for record in records:
        print(record)
```

### Custom Offset

```python
# Start paging from the 100th record
for page in bp.page_query("SELECT Id, Name FROM ACCOUNT", page_size=1000, offset=100):
    records = page.get("queryResponse", [])
    # process records
```

## Notes

- BillingPlatform enforces a 10,000 record limit per page. If you specify a larger `page_size`, it will be capped at 10,000.
- This method automatically handles the correct pagination syntax for BillingPlatform.
- For single-page queries, use the [`query`](query.md) method instead.
- Each yielded page is a dictionary in the same format as the `query` method response.

---

[← Back to Documentation Home](README.md)