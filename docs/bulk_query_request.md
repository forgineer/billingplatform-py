[← Back to Documentation Home](README.md)

# `BillingPlatform.bulk_query_request`

Submit a bulk query request to BillingPlatform for large data retrieval operations.

## Syntax

```python
BillingPlatform.bulk_query_request(
    RequestName: str,
    RequestBody: str,
    RequestsPerBatch: int = 10000,
    ResponseFormat: Literal['CSV', 'JSON'] = "JSON"
) -> dict
```

## Parameters

| Parameter         | Type      | Description                                                                 |
|-------------------|-----------|-----------------------------------------------------------------------------|
| `RequestName`     | `str`     | A name for the bulk query request.                                          |
| `RequestBody`     | `str`     | The ANSI SQL query string to execute in bulk.                               |
| `RequestsPerBatch`| `int`     | Number of records to process per batch (default: 10,000).                   |
| `ResponseFormat`  | `Literal` | Format of the response data, either `"CSV"` or `"JSON"` (default: `"JSON"`).|


## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. Bulk query results are typically found under the `"bulkQueryResponse"` key. |

## Examples

### Submitting a Bulk Query Request

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

sql = "SELECT Id, Name, Status FROM ACCOUNT WHERE Status = 'ACTIVE'"

response = bp.bulk_query_request(
    RequestName="ActiveAccountsBulkQuery",
    RequestBody=sql,
    RequestsPerBatch=5000,
    ResponseFormat="JSON"
)

bulk_results = response.get("bulkQueryResponse", [])
print(bulk_results)
```

## Notes

- Use bulk queries for large datasets to optimize performance and avoid API rate limits.

---

[← Back to Documentation Home](README.md)