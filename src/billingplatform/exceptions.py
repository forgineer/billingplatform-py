from requests import Response


class BillingPlatformException(Exception):
    """Base exception for the Billing Platform."""

    def __init__(self, response: Response, default_message: str = None):
        self.response: Response = response
        self.status_code: int = response.status_code
        self.message: str = response.text or default_message or "An error occurred with the BillingPlatform API."
        super().__init__(f"{self.status_code}: {self.message}")

class BillingPlatform400Exception(BillingPlatformException):
    """Exception for 400 Bad Request errors."""
    def __init__(self, response: Response):
        super().__init__(response, "Bad Request - The request is missing one or more required parameters or contains invalid characters. Correct the request and re-submit the request.")

class BillingPlatform401Exception(BillingPlatformException):
    """Exception for 401 Unauthorized errors."""
    def __init__(self, response: Response):
        super().__init__(response, "Unauthorized - No session ID was provided. To address this, update the HTTP request header to include a valid session ID.")

class BillingPlatform404Exception(BillingPlatformException):
    """Exception for 404 Not Found errors."""
    def __init__(self, response: Response):
        super().__init__(response, "Not Found - This indicates an either an incorrect URL was used for the HTTP request or the request, typically a GET (RETRIEVE in SOAP), did not return any rows that match the query/filters.")

class BillingPlatform429Exception(BillingPlatformException):
    """Exception for 429 Too Many Requests errors."""
    def __init__(self, response: Response):
        super().__init__(response, "Too Many Requests - Too many requests were made within a certain amount of time. Try to space out the API requests to avoid this error.")

class BillingPlatform500Exception(BillingPlatformException):
    """Exception for 500 Internal Server errors."""
    def __init__(self, response: Response):
        super().__init__(response, "Internal Error - See response for details.")
