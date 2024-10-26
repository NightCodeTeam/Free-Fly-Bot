from core.requests_makers import HttpMakerAsync
from core.debug import create_log
from core.dot_env import get_env
from sql.sql_users.sql_users_banned_query import sql_user_in_bans
from .bot_dataclass import Update, Message, Chat, User
from settings import BOT_MAX_UPDATES


class HttpTeleBot(HttpMakerAsync):
    token = get_env('TELEGRAM_BOT_TOKEN')
    last_update = 0

    def __init__(self):
        super().__init__(
            base_url='https://api.telegram.org'
        )

    async def get_updates(self) -> list[Update]:
        res = await self._get(
            url=f'/bot{self.token}/getUpdates',
            params={
                'offset': self.last_update,
                'limit': BOT_MAX_UPDATES
            }
        )
        ans: list[Update] = []
        if res.json['ok']:
            for update in res.json['result']:
                try:
                    if not await sql_user_in_bans(update['message']['from']['id']):
                        ans.append(
                            Update(
                                update_id=update['update_id'],
                                message=Message(
                                    message_id=update['message']['message_id'],
                                    user=User(
                                        id=update['message']['from']['id'],
                                        is_bot=update['message']['from']['is_bot'],
                                        first_name=update['message']['from']['first_name'],
                                        last_name=update['message']['from']['last_name'],
                                        username=update['message']['from']['username'],
                                        language_code=update['message']['from']['language_code'],
                                    ),
                                    chat=Chat(
                                        id=update['message']['chat']['id'],
                                        first_name=update['message']['chat']['first_name'],
                                        last_name=update['message']['chat']['last_name'],
                                        username=update['message']['chat']['username'],
                                        type=update['message']['chat']['type'],
                                    ),
                                    date=update['message']['date'],
                                    text=update['message'].get('text')
                                )
                            )
                        )
                    self.last_update = update['update_id'] + 1

                except KeyError as e:
                    create_log(e, 'error')
        return ans