import requests

from . import exceptions


def response_handler(response: requests.Response) -> dict:
    """
    Handle the response from the BillingPlatform API.

    :param response: The response object from the requests library.
    :return: The response data as a dictionary.
    :raises BillingPlatform400Exception: If the response status code is 400.
    :raises BillingPlatform401Exception: If the response status code is 401.
    :raises BillingPlatform404Exception: If the response status code is 404.
    :raises BillingPlatform429Exception: If the response status code is 429.
    :raises BillingPlatform500Exception: If the response status code is 500.
    :raises BillingPlatformException: If the response status code is not in the range defined above.
    """
    if response.status_code == 400:
        raise exceptions.BillingPlatform400Exception(response)
    elif response.status_code == 401:
        raise exceptions.BillingPlatform401Exception(response)
    elif response.status_code == 404:
        raise exceptions.BillingPlatform404Exception(response)
    elif response.status_code == 429:
        raise exceptions.BillingPlatform429Exception(response)
    elif response.status_code == 500:
        raise exceptions.BillingPlatform500Exception(response)
    else:
        raise exceptions.BillingPlatformException(response)
