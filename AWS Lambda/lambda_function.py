# TODO: Complete Testing
# * test aws slack commander
# * test aws slack slasher
# * test aws api
# * test local api
# * test local slack commander
# * test local slack slasher

import os
import json
import base64
import sys
from urllib.parse import parse_qs

from requests.exceptions import MissingSchema

from load_config import ConfigLoader
from slack import Slack
from gatekeeper import Gatekeeper
from hermes import Hermes
from upload_file import FileUploader

try:
    config_file = 'config_file.json'
    config = ConfigLoader(config_file)
    slack = Slack(config.slack)
    hermes = Hermes(config.hermes)

    gatekeeper = Gatekeeper(config.keys)
    nextcloud = FileUploader(nextcloud=config.nextcloud)

    slack.message.append('Hello from The Gatekeeper!')
except MissingSchema as e:
    print("An error occurred during startup. Check your config")
    sys.exit(1)  # Exit with a non-zero status code to indicate an error


def lambda_handler(event, context):
    print("lambda_handler")
    print(f'An event occurred!\n{event}')
    
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        is_local = False
    else:
        is_local = True

    gatekeeper.is_local = is_local
    nextcloud.is_local = is_local

    # this is only needed when validating slackbot for @ commands (event subscription)
    try:
        if 'body' in event and 'challenge' in event['body']:
            body = json.loads(event['body'])
            challenge = body['challenge']
            return {'statusCode': 200, 'body': challenge}
    except TypeError as e:
        pass

    if not event.get('headers').get('x-slack-retry-num') is None:
        print("returning status 200 to slackbot retry attempt")
        return {"statusCode": 200}

    try:
        if event['isBase64Encoded']:
            slack.target_channel = parse_qs(base64.b64decode(event['body']).decode('utf-8'))['channel_id'][0]
        else:
            slack.target_channel = json.loads(event['body'])['event']['channel']
    except Exception as e:
        print('could not set slack target channel')
        slack.target_channel = slack.default_channel
        print('using default channel')
    finally:
        key = event.get('queryStringParameters').get('apikey')

        if not event.get('headers').get('x-slack-retry-num') is None:
            print('returning status 200 to slackbot retry attempt')
            return_response(200)
        elif gatekeeper.is_key_valid(key):
            if key == gatekeeper.keys['slack_event_key']:
                slack.message.append('Your key has been validated! Welcome Slackbot Commander!')
                if is_local:
                    print('Continuing with local processing')
                    hermes_dispatch(event)
                else:
                    gatekeeper.open_the_gate(event)
                    print('returning status 200 to slackbot event command')
                return_response(200)
            elif key == gatekeeper.keys['slack_command_key']:
                slack.message.append('Your key has been validated! Welcome Slackbot Slasher!')
                if is_local:
                    print('Continuing with local processing')
                    hermes_dispatch(event)
                else:
                    gatekeeper.open_the_gate(event)
                    print('returning status 200 to slackbot slash command')
                return {'statusCode': 200, 'body': 'OK'}
            elif key == gatekeeper.keys['api_command_key']:
                slack.message.append('Your key has been validated! Welcome API Commander!')
                if is_local:
                    print('Continuing with local processing')
                    hermes_dispatch(event)
                else:
                    gatekeeper.open_the_gate(event)
                    print('returning status 200 to api command')
                return {'statusCode': 200, 'body': 'OK'}
            elif key == gatekeeper.keys['hermes_key']:
                slack.message.append('The Gatekeeper has opened the gate for dispatching Hermes with your message!')
                hermes_dispatch(gatekeeper.close_the_gate(event))
            else:
                slack.message.append('The key is not valid!')
                slack.send()
                return_response(403, "forbidden")


def hermes_dispatch(event):
    print("hermes_dispatch")
    slack.message.append('The Gatekeeper has closed the gate after Hermes passed with your message!')
    key = event['queryStringParameters']['apikey']
    if key == gatekeeper.keys['slack_event_key']:
        hermes.get_data_from_slack_event(event)
    if key == gatekeeper.keys['slack_command_key']:
        hermes.get_data_from_slack_command(event)
    if key == gatekeeper.keys['api_command_key']:
        hermes.get_data_from_api_command(event)

    if hermes.is_pattern_valid():
        try:
            channel = slack.target_channel if slack.target_channel else slack.default_channel
            hermes.get_message_object(channel)
            nextcloud.upload(hermes.file_name, json.dumps(hermes.message_object))
            slack.message.append(f'Hermes has promptly delivered your message!\n{json.dumps(hermes.message_object)}')
            slack.send()
            return_response(200, '/n'.join(slack.message))
        except Exception as e:
            slack.message.append(f'Hermes wandered off somewhere and your message never made it!\n{str(e)}')
            slack.send()
            return_response(200, '/n'.join(slack.message))
    else:
        slack.message.append(f'Hermes has return with an undeliverable message because of a misunderstanding!\ninvalid command:\n{hermes.text}')
        slack.send()
        return_response(200, '/n'.join(slack.message))


def return_response(code, body=None):
    print("return_response")
    if body:
        return {'statusCode': code, 'body': body}
    else:
        return {'statusCode': code}
