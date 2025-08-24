import os

from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv
from google.cloud import dialogflow


def get_dialogflow_response(project_id, session_id, text, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return (response.query_result.fulfillment_text or "").strip()


def handle_message(update, context):
    user_text = update.message.text
    session_id = str(update.effective_chat.id)
    project_id = os.getenv('GOOGLE_PROJECT_ID')

    reply = get_dialogflow_response(project_id, session_id, user_text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


def main():
    load_dotenv()
    bot_token = os.getenv('TG_BOT_API')

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
        )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
