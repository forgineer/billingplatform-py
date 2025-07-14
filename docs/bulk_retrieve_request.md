# `BillingPlatform.bulk_retrieve_request`

Submit a bulk retrieve request to BillingPlatform for large-scale record retrieval.

---

## Syntax

```python
BillingPlatform.bulk_retrieve_request(
    RequestName: str,
    RequestBody: str,
    RetrieveEntityName: str,
    Columns: list[str] | None = None,
    RequestsPerBatch: int = 10000,
    CSVDelimiter: str = ',',
    CSVQualifier: str = '"',
    CSVEndLineFormat: Literal['CR', 'LF', 'CRLF'] = "CRLF"
) -> dict
```

---

## Parameters

| Parameter           | Type                | Description                                                                 |
|---------------------|---------------------|-----------------------------------------------------------------------------|
| `RequestName`       | `str`               | A name for the bulk retrieve request.                                       |
| `RequestBody`       | `str`               | The request body, typically an ANSI SQL query or filter.                    |
| `RetrieveEntityName`| `str`               | The name of the entity to retrieve records from (e.g., `"ACCOUNT"`).        |
| `Columns`           | `list[str]` or `None`| List of columns to include in the response. If `None`, all columns are returned. |
| `RequestsPerBatch`  | `int`               | Number of records to process per batch (default: 10,000).                   |
| `CSVDelimiter`      | `str`               | Delimiter character for CSV output (default: `,`).                          |
| `CSVQualifier`      | `str`               | Qualifier character for CSV output (default: `"`).                          |
| `CSVEndLineFormat`  | `Literal`           | End-of-line format for CSV output: `"CR"`, `"LF"`, or `"CRLF"` (default: `"CRLF"`). |

---

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. Bulk retrieve results are typically found under the `"bulkRetrieveResponse"` key. |

---

## Examples

### Submitting a Bulk Retrieve Request

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

response = bp.bulk_retrieve_request(
    RequestName="BulkAccountRetrieve",
    RequestBody="Id > 0",
    RetrieveEntityName="ACCOUNT",
    Columns=["Id", "Name"],
    RequestsPerBatch=5000,
    CSVDelimiter=",",
    CSVQualifier='"',
    CSVEndLineFormat="CRLF"
)

bulk_records = response.get("bulkRetrieveResponse", [])
print(bulk_records)
```

---

## Notes

- Use bulk retrieve for efficient extraction of large datasets.

---

[← Back to Documentation Home](README.md)