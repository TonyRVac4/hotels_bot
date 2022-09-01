import requests


def main_request(url, headers, params):
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
        else:
            raise Exception
    except Exception:
        return ""
