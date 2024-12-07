from core.requests_makers import HttpMakerAsync
from core.debug import create_log
from core.dot_env import get_env
from sql.sql_users.sql_users_banned_query import sql_user_in_bans
from .bot_dataclass import Update, UpdateCallback, Message, Chat, User, CallbackQuery
from settings import BOT_MAX_UPDATES, BOT_TEST_GOODS
import json


class HttpTeleBot(HttpMakerAsync):
    token = get_env('TELEGRAM_BOT_TOKEN')
    last_update = 0

    def __init__(self):
        super().__init__(
            base_url='https://api.telegram.org'
        )

    async def get_updates(self) -> list[Update]:
        res = await self._make(
            url=f'/bot{self.token}/getUpdates',
            method='GET',
            params={
                'offset': self.last_update,
                'limit': BOT_MAX_UPDATES
            }
        )
        ans: list[Update] = []
        if res.json['ok']:
            for update in res.json['result']:
                try:
                    if update.get('message') is not None:
                        if not await sql_user_in_bans(update['message']['from']['id']):
                            ans.append(self.get_update(update))
                    if update.get('callback_query') is not None:
                        if not await sql_user_in_bans(update['callback_query']['from']['id']):
                            ans.append(self.get_update(update))
                except KeyError as e:
                    create_log(e, 'error')
                self.last_update = update['update_id'] + 1
        return ans

    async def sent_msg(self, chat_id: int, message: str, addition_params: dict | None = None) -> bool:
        params = {
            'chat_id': chat_id,
            'text': message
        }
        if addition_params is not None:
            params.update(addition_params)
        return True if (await self._make(
            url=f'/bot{self.token}/sendMessage',
            method='GET',
            params=params,
        )).json['ok'] else False


    async def sent_test_msg(self, chat_id: int, message: str, addition_params: dict | None = None) -> bool:
        params = {
            'chat_id': chat_id,
            'text': message
        }
        data = {
            'reply_markup': json.dumps({
                'inline_keyboard': BOT_TEST_GOODS
                #'inline_keyboard': [[{'text': f'Кнопка {x}', 'callback_data': f'button {x}'}] for x in range(200)]
                #'inline_keyboard': [
                #    [{'text': f'Кнопка {x}', 'callback_data': f'button {x}'} for x in range(100)]
                #    #[
                #    #    {'text': 'Кнопка 1', 'callback_data': 'button1'},
                #    #    {'text': 'Кнопка 2', 'callback_data': 'button2'}
                #    #]
                #]
            })
        }
        if addition_params is not None:
            params.update(addition_params)
        return True if (await self._make(
            url=f'/bot{self.token}/sendMessage',
            method='GET',
            params=params,
            data=data
        )).json['ok'] else False


    async def sent_msg_reply(self, chat_id: int, message: str, message_id: int):
        return await self.sent_msg(
            chat_id=chat_id,
            message=message,
            addition_params={
                'reply_to_message_id': message_id,
                #'reply_parameters': {
                #    'message_id': message_id,
                #},
            }
        )

    @staticmethod
    def get_update(update_dict: dict) -> Update | UpdateCallback:
        if update_dict.get('callback_query') is not None:
            return UpdateCallback(
                update_id=update_dict['update_id'],
                callback_query=CallbackQuery(
                    id=update_dict['callback_query']['id'],
                    user=User(
                        id=update_dict['callback_query']['from']['id'],
                        is_bot=update_dict['callback_query']['from']['is_bot'],
                        first_name=update_dict['callback_query']['from']['first_name'],
                        last_name='',
                        username=update_dict['callback_query']['from']['username'],
                        language_code='',
                    ),
                    message=Message(
                        message_id=update_dict['callback_query']['message']['message_id'],
                        user=User(
                            id=update_dict['callback_query']['message']['from']['id'],
                            is_bot=update_dict['callback_query']['message']['from']['is_bot'],
                            first_name=update_dict['callback_query']['message']['from']['first_name'],
                            last_name='',
                            username=update_dict['callback_query']['message']['from']['username'],
                            language_code='',
                        ),
                        chat=Chat(
                            id=update_dict['callback_query']['message']['chat']['id'],
                            first_name=update_dict['callback_query']['message']['chat']['first_name'],
                            last_name='',
                            username=update_dict['callback_query']['message']['chat']['username'],
                            type=update_dict['callback_query']['message']['chat']['type'],
                        ),
                        date=update_dict['callback_query']['message']['date'],
                        text=update_dict['callback_query']['message'].get('text')
                    ),
                    chat_instance=update_dict['callback_query']['chat_instance'],
                    data=update_dict['callback_query']['data'],
                )
            )
        return Update(
            update_id=update_dict['update_id'],
            message=Message(
                message_id=update_dict['message']['message_id'],
                user=User(
                    id=update_dict['message']['from']['id'],
                    is_bot=update_dict['message']['from']['is_bot'],
                    first_name=update_dict['message']['from']['first_name'],
                    last_name='',
                    username=update_dict['message']['from']['username'],
                    language_code='',
                ),
                chat=Chat(
                    id=update_dict['message']['chat']['id'],
                    first_name=update_dict['message']['chat']['first_name'],
                    last_name='',
                    username=update_dict['message']['chat']['username'],
                    type=update_dict['message']['chat']['type'],
                ),
                date=update_dict['message']['date'],
                text=update_dict['message'].get('text')
            )
        )
