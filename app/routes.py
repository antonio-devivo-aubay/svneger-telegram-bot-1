from flask import request, make_response

import telegram

from app import app, bot
from functools import wraps
import asyncio

from app.credentials import TOKEN, URL, CUSTOM_USERNAME, CUSTOM_PASSWORD, bot_user_name

from app.mastermind import get_response

#
# A simple decorator to protect some public URLs
#
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # FIXME: you should probably implement a better authentication system for production.
        if auth and auth.username == CUSTOM_USERNAME and auth.password == CUSTOM_PASSWORD:
            return f(*args, **kwargs)
        
        return make_response('Could not verify login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

#
# Default URL (not really used)
#
@app.route('/')
@auth_required
def index():
    return "Running {}...".format(bot_user_name)

#
# Set Telegram webhook URL
#
async def set_webhook_async():
    webhook_url = '{URL}{HOOK}'.format(URL=URL, HOOK="WEBHOOK_ROUTE")
    return await bot.setWebhook(url=webhook_url)

async def send_message(chat_id, message):
    timeout = 100000000
    await bot.sendMessage(
        chat_id=chat_id, 
        text=message, 
        read_timeout=timeout,
        write_timeout=timeout,
        connect_timeout=timeout,
        pool_timeout=timeout,
    )

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = asyncio.run(set_webhook_async())

    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

#
# Main Telegram 'callback' URL
#
@app.route('/WEBHOOK_ROUTE', methods=['POST'])
def respond():
    print("sono in respond")
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message is None:
        return 'ok'
    if update.message.chat is None:
        return 'ok'

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text

    if text is not None:
        text = update.message.text.encode('utf-8').decode()
        print("got text message :", text)

        response = get_response(text)
        if response is not None:
            asyncio.run(send_message(chat_id, response))

    return 'ok'