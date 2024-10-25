import aiohttp
from core.debug import create_log
from .requests_dataclasses import ResponseData


class HttpMakerAsync:
    def __init__(self, base_url: str, headers: dict | None = None):
        self._base_url = base_url
        self._headers = headers
        self.__session = aiohttp.ClientSession(base_url=base_url, headers=headers)
    #    self.__update_session()

    #def __update_session(self):
    #    self.__session = aiohttp.ClientSession(
    #        base_url=self._base_url,
    #        headers=self._headers
    #    )

    async def _get(
            self,
            url: str,
            data: dict | None = None,
            json: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> ResponseData | None:
        try:
            async with self.__session.get(
                url=url,
                data=data,
                json=json,
                params=params,
                headers=headers
            ) as response:
                return await self.__get_response_data(response)

        except aiohttp.ClientConnectionError:
            create_log(f'Connection error {self._base_url}{url}', 'error')
            return None

    async def _post(
            self,
            url: str,
            data: dict | None = None,
            json: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> ResponseData | None:
        try:
            async with self.__session.post(
                url=url,
                data=data,
                json=json,
                params=params,
                headers=headers
            ) as response:
                return await self.__get_response_data(response)

        except aiohttp.ClientConnectionError:
            create_log(f'Connection error {self._base_url}{url}', 'error')
            return None

    @staticmethod
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
