import re
import json
import base64

from urllib.parse import parse_qs
from datetime import datetime
from send_message import MessageSender
from upload_file import FileUploader

# passed in as a query parameter for validating access to the funtion
api_token = ""

# required for uploading to nextcloud
nextcloud_username = ""
nextcloud_access_token = ""
nextcloud_url = ""

# dropbox_access_token expires every 4 hours
dropbox_access_token = ""

# required for sending messages as a slackbot
slack_token = ""


def lambda_handler(event, context):
    print('An event occurred!')
    print(event)

    """
    body = json.loads(event['body'])
    challenge = body['challenge']
    return {
        'statusCode':200,
        'body': challenge
    }
    """
    try:
        api_key = event['queryStringParameters']['apikey']
        if api_key == api_token:
            print('The api token has been validated!')
            respond = False
            if event['isBase64Encoded']:
                body = base64.b64decode(event['body']).decode('utf-8')
                parsed_body = parse_qs(body)
                text = parsed_body['text'][0]
                print(f'Received / command: {text}')
            else:
                event_body = json.loads(event['body'])
                text = event_body['event']['blocks'][0]['elements'][0]['elements'][1]['text'].strip()
                team = event_body['event']['team']
                channel = event_body['event']['channel']
                respond = True
                if not event.get('headers').get('x-slack-retry-num') is None:
                    print("returning status code 202 to slackbot retry attempt")
                    return {'statusCode': 200}

            send_message = MessageSender(slack_token)

            match = re.match(r'system\s*(\d+)\s*(.*)', text)
            if match:
                device = f'system{match.group(1)}'
                message = match.group(2)
                timestamp = datetime.now().strftime('%B %d, %Y at %I:%M%p')
                file_name = f'{device}.txt'
                message_object = {
                    'device': device,
                    'message': message,
                    'timestamp': timestamp
                }
                try:
                    upload_file = FileUploader(dropbox_access_token=None, nextcloud_username=nextcloud_username, nextcloud_access_token=nextcloud_access_token,
                                               nextcloud_url=nextcloud_url)
                    upload_file.upload(file_name, json.dumps(message_object))
                    output = f'Hello from Hermes!\nYour message is being promptly delivered!\n{json.dumps(message_object)}'
                    if respond:
                        send_message.slack(output, channel)
                    else:
                        return {
                            'statusCode': 202,
                            'body': f'{output}'
                        }
                except Exception as e:
                    output = 'An internal server error occurred:\n' + str(e)
                    print(output)
                    if respond:
                        send_message.slack(output, channel)
                    else:
                        return {
                            'statusCode': 202,
                            'body': f'{output}'
                        }
            else:
                output = f'The pattern did not match!\ninvalid command:\n{text}'
                if respond:
                    send_message.slack(output, channel)
                else:
                    return {
                        'statusCode': 202,
                        'body': f'{output}'
                    }
        else:
            print('The api token is invalid!')
            return {
                'statusCode': 403,
                'body': 'forbidden'
            }
    except Exception as e:
        print('Unidentified internal server error!')
        print(e)
        return {
            'statusCode': 500,
            'body': 'internal server error'
        }
