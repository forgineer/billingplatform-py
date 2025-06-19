# billingplatform-py

Welcome! This is a community-driven Python library for interacting with BillingPlatform APIs! This project aims to provide a comprehensive and easy-to-use interface for developers working with BillingPlatform.

## Installation

You can install the library using pip:

```bash
pip install billingplatform
```

## Usage

While still under active development towards version 1.0, you can start using the library for its current functionality. Here's a basic example:

```python
from billingplatform import BillingPlatform

# Initialize the API client (creates the session)
# Just in case it has to be said, don't hardcode your credentials in production code ;-)
bp = BillingPlatform(base_url="https://sandbox.billingplatform.com/myorg", username="myuser", password="mypassword")

# Fetch a list of accounts
try:
    response: dict = bp.query(sql="SELECT Id, Name, Status FROM ACCOUNT WHERE 1=1")
    accounts: list[dict] = response.get("queryResponse", []) # Strip out data from response

    for account in accounts:
        print(account)
except Exception as e:
    print(f"An error occurred: {e}")
```

Please note: The available methods and their functionalities are still being expanded. Refer to the source code or future documentation for the most up-to-date usage examples. The tests will also provide a good source for examples.

## Contributions

This is a community-driven project, and we welcome contributions! Whether you're fixing a bug, adding a new feature, improving documentation, or suggesting enhancements, your input is valuable.

If you encounter any issues or have suggestions, please don't hesitate to open an issue on our GitHub Issues page.

We're excited to have you as part of our community as we work towards a robust and complete version 1.0 of this library!