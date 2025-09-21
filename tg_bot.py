import os
from functools import partial

from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv

from logger import setup_logger
from dialogflow_utils import get_dialogflow_response


def handle_message(update, context, project_id):
    try:
        user_text = update.message.text
        session_id = f"tg:u:{update.effective_user.id}"

        reply, _ = get_dialogflow_response(project_id, session_id, user_text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    except Exception:
        logger.exception('handle_message failed')
        raise


def main():
    try:
        load_dotenv()

        logs_dir = os.getenv('LOGS_DIR', 'logs')
        log_file = os.getenv('LOG_FILE', 'bot.log')
        bot_token = os.getenv('TG_BOT_TOKEN')
        project_id = os.getenv('GOOGLE_PROJECT_ID')

        global logger
        logger = setup_logger('TG bot', logs_dir, log_file)

        updater = Updater(token=bot_token, use_context=True)
        dispatcher = updater.dispatcher

        bound_message_handler = partial(handle_message, project_id=project_id)

        dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, bound_message_handler)
            )

        logger.info('TG bot start!')

        updater.start_polling()
        updater.idle()
    except Exception as e:
        logger.critical(e, exc_info=True)
        raise


if __name__ == '__main__':
    main()
