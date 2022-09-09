import requests
from loguru import logger


def main_request(url, headers, params):
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == requests.codes.ok and response.text:
            return response
        raise ValueError
    except ValueError as esp:
        logger.exception(esp)
        return ""
