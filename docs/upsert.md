[← Back to Documentation Home](README.md)

# `BillingPlatform.upsert`

Create or update records in BillingPlatform for a specified entity, using an external ID field to determine uniqueness.

## Syntax

```python
BillingPlatform.upsert(entity: str, data: list[dict] | dict, externalIDFieldName: str) -> dict
```

## Parameters

| Parameter            | Type             | Description                                                                 |
|----------------------|------------------|-----------------------------------------------------------------------------|
| `entity`             | `str`            | The name of the entity to upsert records for (e.g., `"ACCOUNT"`).           |
| `data`               | `dict` or `list` | The record data to upsert. Can be a single dict or a list of dicts.         |
| `externalIDFieldName`| `str`            | The field name used to match records for upsert operations.                 |

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The upserted records are typically found under the `"upsertResponse"` key. |

## Examples

### Upserting a Single Record

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

payload = {
    "ExternalId": "EXT-12345",
    "Name": "Upserted Account",
    "Status": "ACTIVE"
}

response = bp.upsert(entity="ACCOUNT", data=payload, externalIDFieldName="ExternalId")
upserted = response.get("upsertResponse", [])
print(upserted)
```

### Upserting Multiple Records

```python
accounts = [
    {"ExternalId": "EXT-12345", "Name": "Account 1", "Status": "ACTIVE"},
    {"ExternalId": "EXT-67890", "Name": "Account 2", "Status": "INACTIVE"}
]

response = bp.upsert(entity="ACCOUNT", data=accounts, externalIDFieldName="ExternalId")
upserted_accounts = response.get("upsertResponse", [])
```

## Notes

- The `data` parameter will be wrapped in a `"brmObjects"` key if not already present.
- The `externalIDFieldName` must match a field in your BillingPlatform entity that is used for upsert matching.

---

[← Back to Documentation Home](README.md)