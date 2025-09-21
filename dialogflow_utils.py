from google.cloud import dialogflow


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
