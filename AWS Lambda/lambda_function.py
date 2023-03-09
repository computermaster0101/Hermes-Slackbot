import json

from load_config import ConfigLoader
from slack import Slack
from gatekeeper import Gatekeeper
from hermes import Hermes
from upload_file import FileUploader

config_file = 'config_file.json'
config = ConfigLoader(config_file)

slack = Slack(config.slack)
gatekeeper = Gatekeeper(config.keys)
hermes = Hermes(config.hermes)
nextcloud = FileUploader(nextcloud=config.nextcloud)


def lambda_handler(event, context):
    print("lambda_handler")
    print(f'An event occurred!\n{event}')

    """
    # this is only needed when validating slackbot for @ commands (event subscription)
    body = json.loads(event['body'])
    challenge = body['challenge']
    return {
        'statusCode':200,
        'body': challenge
    }
    """
    slack.target_channel = json.loads(event['body'])['event']['channel']
    slack.message.append('Hello from The Gatekeeper!')

    if not event.get('headers').get('x-slack-retry-num') is None:
        # slack.message.append('A duplicate message was received!')
        # slack.send()
        print('returning status 200 to slackbot retry attempt')
        return_response(200)

    key = event['queryStringParameters']['apikey']
    if gatekeeper.is_key_valid(key):
        slack.message.append('The key has been validated!')
        if key == gatekeeper.keys['slack_event_key']:
            slack.message.append('Welcome Slackbot Commander!')
            gatekeeper.open_the_gate(event)
            slack.send()
            print('returning status 200 to slackbot event command')
            return_response(200)
        elif key == gatekeeper.keys['slack_command_key']:
            slack.message.append('Welcome Slackbot Slasher!')
            gatekeeper.open_the_gate(event)
            slack.send()
            print('returning status 200 to slackbot slash command')
            return_response(200)
        elif key == gatekeeper.keys['hermes_key']:
            slack.message.append('Welcome Hermes!')
            hermes_dispatch(gatekeeper.close_the_gate(event))
        else:
            slack.message.append('The key is invalid!')
            slack.send()
            return_response(403, "forbidden")


def hermes_dispatch(event):
    print("hermes_dispatch")
    key = event['queryStringParameters']['apikey']
    if key == gatekeeper.keys['slack_event_key']:
        hermes.get_data_from_slack_event(event)
    if key == gatekeeper.keys['slack_command_key']:
        hermes.get_data_from_slack_command(event)

    if hermes.is_pattern_valid():
        try:
            channel = slack.target_channel if slack.target_channel else slack.default_channel
            hermes.get_message_object(channel)
            nextcloud.upload(hermes.file_name, json.dumps(hermes.message_object))
            slack.message.append(f'Your message is being promptly delivered!\n{json.dumps(hermes.message_object)}')
            slack.send()
            body='\n'.join(slack.message)
            return_response(200, '/n'.join(slack.message))
        except Exception as e:
            slack.message.append('An internal server error occurred:\n' + str(e))
            slack.send()
            body='\n'.join(slack.message)
            return_response(200, '/n'.join(slack.message))
    else:
        slack.message.append(f'The pattern did not match!\ninvalid command:\n{hermes.text}')
        slack.send()
        body='\n'.join(slack.message)
        return_response(200, '/n'.join(slack.message))


def return_response(code, body=None):
    print("return_response")
    if body:
        return {'statusCode': code, "body": body}
    else:
        return {'statusCode': code}
