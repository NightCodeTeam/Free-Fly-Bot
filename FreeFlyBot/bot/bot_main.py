from core.requests_makers import maker_async_get, maker_async_post
from core.debug import create_log
from core.dot_env import get_env
from pprint import pprint


class Bot:
    token = get_env('TELEGRAM_BOT_TOKEN')

    async def get_updates(self):
        results = await maker_async_get(
            f'https://api.telegram.org/bot{self.token}/getUpdates',
        )
        pprint(results.json)
