from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name,URL


TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


@app.route('/')
def hello():
    return "Index page is up!"


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    global text
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    response = get_response(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

def get_response(msg):
    """
    Generate a response whenever the bot recieves a message

    """
    return "Message Received: " + text

    
if __name__ == '__main__':
    app.run(threaded=True)