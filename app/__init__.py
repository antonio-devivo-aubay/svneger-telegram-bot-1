from flask import Flask
import telegram
from dotenv import load_dotenv
import os

#Load env variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE_PATH = os.path.join(SCRIPT_DIR, ".env")
load_dotenv(ENV_FILE_PATH)

from app.credentials import TOKEN

app = Flask(__name__)

bot = telegram.Bot(token=TOKEN)

from app import routes
