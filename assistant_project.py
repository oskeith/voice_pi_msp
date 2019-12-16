#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

# google assistant imports
import logging
import platform
import sys

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led

# dialogflow imports
import dialogflow_v2 as dialogflow
import os
from google.api_core.exceptions import InvalidArgument

# dialogflow globals
DIALOGFLOW_PROJECT_ID = 'p461-language-sqtqac'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser('~/dialogflow.json')
SESSION_ID = 'dam-bl0ck'

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

def df_process(text_to_be_analyzed):
    global session
    
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    
    return response

def states(response):
    detected_intent = response.query_result.intent.display_name
    if detected_intent == "servo_command":
        servo_angle = response.query_result.parameters.values()[0]
        print(servo_angle)
##    print(response.query_result.parameters.values())
##    print(response.query_result.parameters.keys())
##    print(response.query_result.parameters.items())
##    print("Query text:", response.query_result.query_text)
##    print("Detected intent:", response.query_result.intent.display_name)
##    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
##    print("Fulfillment text:", response.query_result.fulfillment_text)

def process_event(led, event):
    logging.info(event)

    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        logging.info('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Listening.

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        led.state = Led.BEACON_DARK
        
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        heard_text = event.args["text"]
        if heard_text != "":
            df_response = df_process(heard_text)
            states(df_response)

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    logging.basicConfig(level=logging.INFO)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(board.led, event)


if __name__ == '__main__':
    main()