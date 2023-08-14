import requests


def get_response_code_url(url: str) -> int:
    response = requests.get(url)
    return response.status_code
