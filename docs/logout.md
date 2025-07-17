[← Back to Documentation Home](README.md)

# `BillingPlatform.logout`

Log out of the BillingPlatform API and close the current session.

## Syntax

```python
BillingPlatform.logout() -> None
```

## Parameters

This method does not take any parameters.

## Returns

| Type   | Description |
|--------|-------------|
| `None` | This method does not return a value. It closes the session and logs out from BillingPlatform. |

## Examples

### Logging Out

```python
from billingplatform import BillingPlatform

bp = BillingPlatform(
    base_url="https://sandbox.billingplatform.com/myorg",
    username="your_username",
    password="your_password"
)

# ... perform API operations ...

bp.logout()  # Log out and close the session
```

## Notes

- This method is automatically called at exit or at the end of your script by default with the `logout_at_exit` parameter set to `True` upon initialization of the `BillingPlatform` object.
- If `logout_at_exit` is set to `False` on initialization, you must call `logout()` manually to logout of your session.
- Logging out of your session is considered best practice by BillingPlatform.

---

[← Back to Documentation Home](README.md)