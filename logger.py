import logging
import os
import traceback
from logging.handlers import RotatingFileHandler

from telegram import Bot


class LogHandler(logging.Handler):
    def __init__(self, bot_token, chat_id):
        super().__init__()

        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        try:
            formatted_record = self.format(record)
            if record.exc_info:
                text = '\n'.join(traceback.format_exception(*record.exc_info))
                formatted_record += f"\nTraceback:\n{text}"

            self.bot.send_message(
                chat_id=self.chat_id,
                text=formatted_record,
                parse_mode=None
            )

        except Exception as e:
            print(f"Ошибка при отправке лога: {e}")


def create_log_file(logs_dir, log_file):
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, log_file)

    log_file = RotatingFileHandler(
        filename=log_path,
        maxBytes=1024*1024,
        backupCount=3,
        encoding='utf-8'
    )

    return log_file


def setup_logger(name, logs_dir, log_file, log_bot_token=None, log_chat_id=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = create_log_file(logs_dir, log_file)

    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)

    if log_bot_token and log_chat_id:
        tg_vk_handler = LogHandler(log_bot_token, log_chat_id)
        tg_vk_handler.setLevel(logging.ERROR)
        logger.addHandler(tg_vk_handler)

    return logger
