import telepot

secret = "efe651ce-826e-4c6a-97a2-46a1d54c306d"
bot = telepot.Bot('705147392:AAFKi_wCIILco9EnoLaykGb3coUWicOueEg')


def setWebhook():
    bot.setWebhook("http://ewtm.ru/managing/telegram/{0}".format(secret), max_connections=1)
    return True

def telegram_webhook(update):
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            bot.sendMessage(chat_id, "From the web: you said '{}'".format(text))
        else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")
    return "OK"