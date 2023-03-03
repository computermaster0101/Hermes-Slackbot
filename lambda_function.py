import re
import json
import base64
import urllib.parse
import urllib.request
from urllib.parse import parse_qs
from datetime import datetime
from upload_file import FileUploader

api_token="Vsu9TRxpQ4cMIwvs409GJzzjcLPHNtduu5SWMChNregJ1UdoSNnwThsUtSvpxinV"
dropbox_access_token="sl.BZ2KV65_29wX3hTieM1s404IyYiwBpnWhJsfXBVLTqb1GYfiYJZaSwbRNY6A5vq5WGzR0mANgUwjVabYjDOaF70n0mJK5UxxPfhZchmAk1jqFx5Kshg-JAV0S872KotYW2S3PqI"


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
            method=""
            if event['isBase64Encoded']:
                body = base64.b64decode(event['body']).decode('utf-8')
                parsed_body = parse_qs(body)
                text = parsed_body['text'][0]
                print(f'Received / command: {text}')
                method='slash'
            else:
                text = json.loads(event['body'])['event']['blocks'][0]['elements'][0]['elements'][1]['text'].strip()
                print(f'Received @ command: {text}')
                method='at'

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
                    upload_file = FileUploader(dropbox_access_token=dropbox_access_token)
                    upload_file.dropbox(file_name, json.dumps(message_object))
                    output=f'Hello from Hermes!\nYour message is being promptly delivered!\n{json.dumps(message_object)}'
                    select_message_return_method(method,output)
                    return {
                        'statusCode': 202,
                        'body': f'{output}'
                    }
                except Exception as e:
                    output='An internal server error occurred:\n' + str(e)
                    select_message_return_method(method,output)
                    return {
                        'statusCode': 202,
                        'body': f'{output}'
                    }
            else:
                output=f'The pattern did not match!\ninvalid command:\n{text}'
                select_message_return_method(method,output)
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

def select_message_return_method(method, message):
    print(message)
    if method == "at":
        return send_message_to_slack(message)

def return_message_to_slack(message):
    return {
        'statusCode': 202,
        'body': 'static string for testing'
    }

def send_message_to_slack(message):
    slack_url="https://slack.com/api/chat.postMessage"
    channel_id="C04S2PX6U9K"
    token="xoxb-1620285266083-4876057954115-NQ512QTznSI7fz02lKWM32EB"

    data = urllib.parse.urlencode(
        (
            ("token", token),
            ("channel", channel_id),
            ("text", message)
        )
    )
    data = data.encode("ascii")

    request = urllib.request.Request(slack_url, data=data, method="POST")
    request.add_header( "Content-Type", "application/x-www-form-urlencoded")
    x = urllib.request.urlopen(request).read()
    print(x)
    return { 'statusCode': 202 }
