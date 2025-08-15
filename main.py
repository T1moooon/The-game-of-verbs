import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():
    load_dotenv()
    bot_token = os.getenv('TG_BOT_API')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
