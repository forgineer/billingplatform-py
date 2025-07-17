[← Back to Documentation Home](README.md)]

# `BillingPlatform.create`

Create new records in BillingPlatform for a specified entity.

## Syntax

```python
BillingPlatform.create(entity: str, data: list[dict] | dict) -> dict
```

## Parameters

| Parameter | Type             | Description                                                      |
|-----------|------------------|------------------------------------------------------------------|
| `entity`  | `str`            | The name of the entity to create records for (e.g., `"ACCOUNT"`).|
| `data`    | `dict` or `list` | The record data to create. Can be a single dict or a list of dicts.|

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The created records are typically found under the `"createResponse"` key. |

## Examples

### Creating a Single Record

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

payload = {
    "Name": "Test Account",
    "Status": "ACTIVE"
}

response = bp.create(entity="ACCOUNT", data=payload)
created = response.get("createResponse", [])
print(created)
```

### Creating Multiple Records

```python
accounts = [
    {"Name": "Account 1", "Status": "ACTIVE"},
    {"Name": "Account 2", "Status": "INACTIVE"}
]

response = bp.create(entity="ACCOUNT", data=accounts)
created_accounts = response.get("createResponse", [])
```

## Notes

- The `data` parameter will be wrapped in a `"brmObjects"` key if not already present.

---

[← Back to Documentation Home](README.md)