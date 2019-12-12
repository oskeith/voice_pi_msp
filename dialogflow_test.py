import dialogflow_v2 as dialogflow
import os
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = 'p461-language-sqtqac'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
#GOOGLE_APPLICATION_CREDENTIALS = os.path.expanduser('~/dialogflow.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser('~/dialogflow.json')
SESSION_ID = 'dam-bl0ck'

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

text_to_be_analyzed = "garbled mess"

text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
response = session_client.detect_intent(session=session, query_input=query_input)

try:
    response = session_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raise

print("Query text:", response.query_result.query_text)
print("Detected intent:", response.query_result.intent.display_name)
print("Detected intent confidence:", response.query_result.intent_detection_confidence)
print("Fulfillment text:", response.query_result.fulfillment_text)