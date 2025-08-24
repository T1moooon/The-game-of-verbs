import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id):
    with open('questions.json', 'r', encoding='utf-8') as json_file:
        question_json = json.load(json_file)

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    existing = {i.display_name for i in intents_client.list_intents(request={"parent": parent})}

    created_intents = []

    for intent_name, intent_text in question_json.items():
        training_phrases = []

        if intent_name in existing:
            continue

        for phrase in intent_text['questions']:
            part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        message_texts = [intent_text["answer"]]
        text = dialogflow.Intent.Message.Text(text=message_texts)
        message = dialogflow.Intent.Message(text=text)

        intent = dialogflow.Intent(
            display_name=intent_name,
            training_phrases=training_phrases,
            messages=[message]
        )

        response = intents_client.create_intent(
            request={'parent': parent, 'intent': intent}
        )
        created_intents.append(intent_name)

    return created_intents


if __name__ == '__main__':
    load_dotenv()

    project_id = os.getenv('GOOGLE_PROJECT_ID')

    intents = create_intent(project_id)
    for intent in intents:
        print(f'"{intent}" создан!')
