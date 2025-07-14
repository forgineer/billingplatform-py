# `BillingPlatform.query`

Query records from BillingPlatform using an ANSI SQL statement.

---

## Syntax

```python
BillingPlatform.query(sql: str) -> dict
```

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sql`     | `str` | The ANSI SQL query string to execute against the BillingPlatform API. |

---

## Returns

| Type   | Description |
|--------|-------------|
| `dict` | The response data from BillingPlatform. The main results are typically found under the `"queryResponse"` key. |

---

## Examples

### Basic Usage

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

response = bp.query("SELECT Id, Name, Status FROM ACCOUNT WHERE Status = 'ACTIVE'")
accounts = response.get("queryResponse", [])
for account in accounts:
    print(account)
```

---

### Filtering Results

```python
sql = "SELECT Id, Name FROM ACCOUNT WHERE Status = 'INACTIVE'"
response = bp.query(sql)
inactive_accounts = response.get("queryResponse", [])
```

---

## Notes

- The SQL syntax must be supported by BillingPlatform's API. Refer to the official BillingPlatform documentation for supported SQL features.

---

[← Back to Documentation Home](README.md)