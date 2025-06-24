from requests import Response


class BillingPlatformException(Exception):
    """Base exception for the Billing Platform."""

    def __init__(self, response: Response):
        super().__init__(response.text)
        self.response: Response = response

class BillingPlatform400Exception(BillingPlatformException):
    """Exception for 400 Bad Request errors."""

class BillingPlatform401Exception(BillingPlatformException):
    """Exception for 401 Unauthorized errors."""

class BillingPlatform404Exception(BillingPlatformException):
    """Exception for 404 Not Found errors."""

class BillingPlatform429Exception(BillingPlatformException):
    """Exception for 429 Too Many Requests errors."""

class BillingPlatform500Exception(BillingPlatformException):
    """Exception for 500 Internal Server errors."""
