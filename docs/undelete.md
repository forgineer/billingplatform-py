[← Back to Documentation Home](README.md)

# `BillingPlatform.undelete`

Restore (undelete) records in BillingPlatform for a specified entity.

## Syntax

```python
BillingPlatform.undelete(entity: str, data: list[dict] | dict) -> dict
```

## Parameters

| Parameter | Type             | Description                                                      |
|-----------|------------------|------------------------------------------------------------------|
| `entity`  | `str`            | The name of the entity to restore records for (e.g., `"ACCOUNT"`).|
| `data`    | `dict` or `list` | The record data to restore. Can be a single dict or a list of dicts.|

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The restored records are typically found under the `"undeleteResponse"` key. |

## Examples

### Restoring a Single Record

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

payload = {
    "Id": 12345
}

response = bp.undelete(entity="ACCOUNT", data=payload)
restored = response.get("undeleteResponse", [])
print(restored)
```

### Restoring Multiple Records

```python
accounts = [
    {"Id": 12345},
    {"Id": 67890}
]

response = bp.undelete(entity="ACCOUNT", data=accounts)
restored_accounts = response.get("undeleteResponse", [])
```

## Notes

- The `data` parameter will be wrapped in a `"brmObjects"` key if not already present.

---

[← Back to Documentation Home](README.md)