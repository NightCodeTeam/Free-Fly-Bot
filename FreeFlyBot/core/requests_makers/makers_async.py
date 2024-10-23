import aiohttp
from core.debug import create_log
from .requests_dataclasses import ResponseData


async def maker_async_get(
        url: str,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
) -> ResponseData | None:
    try:
        return await __get_response_data(aiohttp.get(
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers
        ))
    except aiohttp.exceptions.ConnectionError:
        create_log(f'Connection error {url}', 'error')
        return None


async def maker_async_post(
        url: str,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
) -> ResponseData | None:
    try:
        return await __get_response_data(aiohttp.post(
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers
        ))
    except aiohttp.exceptions.ConnectionError:
        create_log(f'Connection error {url}', 'error')
        return None


async def __get_response_data(response: aiohttp.Response) -> ResponseData:
    try:
        data = await response.json()
        if type(data) is not dict:
            data = {'data': data}
    except (
        aiohttp.exceptions.ContentDecodingError,
        aiohttp.exceptions.JSONDecodeError
    ) as e:
        create_log(e, 'error')
        data = {'error': await response.text}
    return ResponseData(
        response.status_code,
        data
    )
