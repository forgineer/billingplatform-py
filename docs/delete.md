# `BillingPlatform.delete`

Delete records in BillingPlatform for a specified entity.

---

## Syntax

```python
BillingPlatform.delete(entity: str, data: list[dict] | dict, EmptyRecycleBin: bool = False) -> dict
```

---

## Parameters

| Parameter         | Type             | Description                                                                 |
|-------------------|------------------|-----------------------------------------------------------------------------|
| `entity`          | `str`            | The name of the entity to delete records from (e.g., `"ACCOUNT"`).          |
| `data`            | `dict` or `list` | The record data to delete. Can be a single dict or a list of dicts.         |
| `EmptyRecycleBin` | `bool`           | If `True`, permanently deletes records instead of moving them to recycle bin.|

---

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The deleted records are typically found under the `"deleteResponse"` key. |

---

## Examples

### Deleting a Single Record

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

response = bp.delete(entity="ACCOUNT", data=payload)
deleted = response.get("deleteResponse", [])
print(deleted)
```

---

### Deleting Multiple Records and Emptying Recycle Bin

```python
accounts = [
    {"Id": 12345},
    {"Id": 67890}
]

response = bp.delete(entity="ACCOUNT", data=accounts, EmptyRecycleBin=True)
deleted_accounts = response.get("deleteResponse", [])
```

---

## Notes

- The `data` parameter will be wrapped in a `"brmObjects"` key if not already present.

---

[← Back to Documentation Home](README.md)