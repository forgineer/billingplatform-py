[← Back to Documentation Home](README.md)

# `BillingPlatform.update`

Update existing records in BillingPlatform for a specified entity.

## Syntax

```python
BillingPlatform.update(entity: str, data: list[dict] | dict) -> dict
```

## Parameters

| Parameter | Type             | Description                                                      |
|-----------|------------------|------------------------------------------------------------------|
| `entity`  | `str`            | The name of the entity to update records for (e.g., `"ACCOUNT"`).|
| `data`    | `dict` or `list` | The record data to update. Can be a single dict or a list of dicts.|

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The updated records are typically found under the `"updateResponse"` key. |

## Examples

### Updating a Single Record

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

payload = {
    "Id": 12345,
    "Name": "Updated Account Name",
    "Status": "ACTIVE"
}

response = bp.update(entity="ACCOUNT", data=payload)
updated = response.get("updateResponse", [])
print(updated)
```

### Updating Multiple Records

```python
accounts = [
    {"Id": 12345, "Name": "Account 1 Updated", "Status": "ACTIVE"},
    {"Id": 67890, "Name": "Account 2 Updated", "Status": "INACTIVE"}
]

response = bp.update(entity="ACCOUNT", data=accounts)
updated_accounts = response.get("updateResponse", [])
```

## Notes

- The `data` parameter will be wrapped in a `"brmObjects"` key if not already present.

---

[← Back to Documentation Home](README.md)