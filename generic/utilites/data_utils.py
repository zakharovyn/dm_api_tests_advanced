from requests import Response, JSONDecodeError


def get_json(response: Response):
    try:
        return response.json()
    except JSONDecodeError:
        return None
