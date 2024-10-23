import requests
from core.debug import create_log
from .requests_dataclasses import ResponseData


def maker_get(
        url: str,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
) -> ResponseData | None:
    try:
        return __get_response_data(requests.get(
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers
        ))
    except requests.exceptions.ConnectionError:
        create_log(f'Connection error {url}', 'error')
        return None


def maker_post(
        url: str,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
) -> ResponseData | None:
    try:
        return __get_response_data(requests.post(
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers
        ))
    except requests.exceptions.ConnectionError:
        create_log(f'Connection error {url}', 'error')
        return None


def __get_response_data(response: requests.Response) -> ResponseData:
    try:
        data = response.json()
        if type(data) is not dict:
            data = {'data': data}
    except (
        requests.exceptions.ContentDecodingError,
        requests.exceptions.JSONDecodeError
    ) as e:
        create_log(e, 'error')
        data = {'error': response.text}
    return ResponseData(
        response.status_code,
        data
    )
