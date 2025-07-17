[← Back to Documentation Home](README.md)

# `BillingPlatform.retrieve_by_id`

Retrieve a single record from BillingPlatform by entity name and record ID.

## Syntax

```python
BillingPlatform.retrieve_by_id(entity: str, record_id: int) -> dict
```

## Parameters

| Parameter    | Type   | Description                                              |
|--------------|--------|----------------------------------------------------------|
| `entity`     | `str`  | The name of the entity to retrieve (e.g., `"ACCOUNT"`).  |
| `record_id`  | `int`  | The unique identifier of the record to retrieve.         |

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The main record is typically found under the `"retrieveResponse"` key. |

## Examples

### Basic Usage

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

response = bp.retrieve_by_id(entity="ACCOUNT", record_id=12345)
record = response.get("retrieveResponse", {})
print(record)
```

## Notes

- The `entity` parameter should match the BillingPlatform object type you

---

[← Back to Documentation Home](README.md)