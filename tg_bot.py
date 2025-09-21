import os

from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv

from logger import setup_logger
from dialogflow_utils import get_dialogflow_response


def handle_message(update, context):
    try:
        user_text = update.message.text
        session_id = str(update.effective_chat.id)
        project_id = os.getenv('GOOGLE_PROJECT_ID')

        reply, _ = get_dialogflow_response(project_id, session_id, user_text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    except Exception:
        logger.exception('handle_message failed')


def main():
    try:
        load_dotenv()

        logs_dir = os.getenv('LOGS_DIR', 'logs')
        log_file = os.getenv('LOG_FILE', 'bot.log')
        bot_token = os.getenv('TG_BOT_TOKEN')

        global logger
        logger = setup_logger('TG bot', logs_dir, log_file)

        updater = Updater(token=bot_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, handle_message)
            )

        logger.info('TG bot start!')

        updater.start_polling()
        updater.idle()
    except Exception as e:
        logger.critical(e, exc_info=True)


if __name__ == '__main__':
    main()
