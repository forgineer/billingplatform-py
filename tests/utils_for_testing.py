import json


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
