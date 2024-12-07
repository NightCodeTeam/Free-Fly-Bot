import aiohttp
from core.debug import create_log
from .makers_exceptions import RequestMethodNotFoundException
from .requests_dataclasses import ResponseData, Method


class HttpMakerAsync:
    def __init__(self, base_url: str, headers: dict | None = None):
        self._base_url = base_url
        self._headers = headers
        self.__session = aiohttp.ClientSession(base_url=base_url, headers=headers)

    async def close_session(self):
        await self.__session.close()

    def __del__(self):
        pass
        #del self.__session

    async def _make(
            self,
            url: str,
            method: Method,
            data: dict | None = None,
            json: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> ResponseData | None:
        try:
            res = None
            # ! Делаем запрос
            match method:
                case 'GET':
                    res = await self.__session.get(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
                case 'POST':
                    res = await self.__session.post(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
                case 'PUT':
                    res = await self.__session.put(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
                case 'DELETE':
                    res = await self.__session.delete(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
            if res is not None:
                return await self.__get_response_data(res)
            raise RequestMethodNotFoundException(method)
        except aiohttp.exceptions.ConnectionError:
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
