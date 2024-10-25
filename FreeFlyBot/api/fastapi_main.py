import fastapi
import uvicorn
from core.debug import create_log
from core.dot_env import get_env
from bot_tele.bot_main import TeleBot


class ServerMain:
    app = fastapi.FastAPI()
    bot_tele = TeleBot()

    def run(self):
        create_log('Starting API')
        uvicorn.run(
            self.app,
            host=get_env('FASTAPI_HOST'),
            port=int(get_env('FASTAPI_PORT')),
            reload=True
        )