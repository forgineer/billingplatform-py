import json


"""
Tests assume a 'credentials.json' file exists withthe following structure:

{
    "login": {
        "base_url": "https://sandbox.billingplatform.com/<your_environment>",
        "username": "your_username",
        "password": "your_password"
    },
    "oauth": {
        "base_url": "https://sandbox.billingplatform.com/<your_environment>",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret"
    }
}

If using the mock server, the base_url would likely be set to http://localhost:5000
"""

def get_credentials(file_path='credentials.json', *keys) -> dict:
    """
    Load credentials from a JSON file. Select specific key/value pairs if provided.

    :param file_path: Path to the JSON credentials file.
    :param keys: Optional keys to navigate through nested dictionaries.
    :return: Dictionary containing the selected credentials.
    """
    with open(file_path) as f:
        credentials: dict = json.load(f)

        for key in keys:
            if key not in credentials:
                raise KeyError(f"Key '{key}' not found in credentials file.")
            credentials = credentials[key]
        
        return credentials
