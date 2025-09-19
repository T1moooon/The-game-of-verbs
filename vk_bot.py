import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow

from logger import setup_logger


def get_dialogflow_response(project_id, session_id, text, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    fulfillment = (response.query_result.fulfillment_text or "").strip()
    is_fallback = bool(response.query_result.intent.is_fallback)

    return fulfillment, is_fallback


def send_message(vk_api, event, text):
    try:
        if event.from_user:
            vk_api.messages.send(
                user_id=event.user_id,
                message=text,
                random_id=random.randint(1, 1000)
            )
        elif event.from_chat:
            vk_api.messages.send(
                chat_id=event.chat_id,
                message=text,
                random_id=random.randint(1, 1000)
            )
    except Exception:
        logger.exception('send message')


def main():
    try:
        load_dotenv()

        logs_dir = os.getenv('LOGS_DIR', 'logs')
        log_file = os.getenv('LOG_FILE', 'bot.log')
        vk_session = vk.VkApi(token=os.getenv("VK_BOT_API"))
        project_id = os.getenv("GOOGLE_PROJECT_ID")

        global logger
        logger = setup_logger('VK bot', logs_dir, log_file)

        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        logger.info("VK bot start!")

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = (event.text or "").strip()
                session_id = event.user_id if event.from_user else event.chat_id

                reply, is_fallback = get_dialogflow_response(
                    project_id=project_id,
                    session_id=session_id,
                    text=text,
                    language_code="ru-RU"
                )

                if is_fallback or not reply:
                    continue

                send_message(vk_api, event, reply)
    except Exception as e:
        logger.critical(e, exc_info=True)


if __name__ == "__main__":
    main()
