from flask import Flask
import telegram
from dotenv import load_dotenv
import os
import asyncio

#Load env variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE_PATH = os.path.join(SCRIPT_DIR, ".env")
load_dotenv(ENV_FILE_PATH)

from credentials import TOKEN

app = Flask(__name__)

bot = telegram.Bot(token=TOKEN)

import routes

async def set_webhook():
    webhook_url = 'https://localhost:8443/WEBHOOK_ROUTE'
    await bot.setWebhook(url=webhook_url)

if __name__ == '__main__':
    # Configura l'URL del webhook
    asyncio.run(set_webhook())

    # Esegui l'applicazione Flask
    app.run(port=8443)