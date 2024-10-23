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
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                data=data,
                json=json,
                params=params,
                headers=headers
            ) as response:
                print(response.url)
                return await __get_response_data(response)

    except aiohttp.ClientConnectionError:
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
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=url,
                data=data,
                json=json,
                params=params,
                headers=headers
            ) as response:
                return await __get_response_data(response)

    except aiohttp.ClientConnectionError:
        create_log(f'Connection error {url}', 'error')
        return None


async def __get_response_data(response: aiohttp.ClientResponse) -> ResponseData:
    try:
        data = await response.json()
        if type(data) is not dict:
            data = {'data': data}
    except aiohttp.ContentTypeError as e:
        create_log(e, 'error')
        data = {'error': await response.text()}
    return ResponseData(
        response.status,
        data
    )
