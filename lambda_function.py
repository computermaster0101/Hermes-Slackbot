import re
import json
import base64
import urllib.parse
import urllib.request
from urllib.parse import parse_qs
from datetime import datetime

api_token = ""
dropbox_access_token = ""


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
            elif json.loads(event['body'])['event']['text']:
                method = 'at'
                event_body = json.loads(event['body'])
                text = event_body['event']['text']
                team = event_body['event']['team']
                channel = event_body['event']['channel']
                respond = True
            else:
                event_body = json.loads(event['body'])
                text = event_body['event']['blocks'][0]['elements'][0]['elements'][1]['text'].strip()
                team = event_body['event']['team']
                channel = event_body['event']['channel']
                respond = True

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
                    output = f'Hello from Hermes!\nYour message is being promptly delivered!\n{json.dumps(message_object)}'
                    if respond:
                        send_message_to_slack(output, channel)
                    else:
                        return {
                            'statusCode': 202,
                            'body': f'{output}'
                        }
                except Exception as e:
                    output = 'An internal server error occurred:\n' + str(e)
                    if respond:
                        send_message_to_slack(output, channel)
                    else:
                        return {
                            'statusCode': 202,
                            'body': f'{output}'
                        }
            else:
                output = f'The pattern did not match!\ninvalid command:\n{text}'
                if respond:
                    send_message_to_slack(output, channel)
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


def send_message_to_slack(message, channel):
    slack_url = "https://slack.com/api/chat.postMessage"
    token = ""

    data = urllib.parse.urlencode(
        (
            ("token", token),
            ("channel", channel),
            ("text", message)
        )
    )
    data = data.encode("ascii")

    request = urllib.request.Request(slack_url, data=data, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    x = urllib.request.urlopen(request).read()
    print(x)
    return {'statusCode': 202}


import os
import dropbox


class FileUploader:
    def __init__(self, dropbox_access_token):
        self.dbx = dropbox.Dropbox(dropbox_access_token)

    def dropbox(self, file_name, content):
        tmp_file_path = os.path.join('/tmp', file_name)
        with open(tmp_file_path, 'w') as f:
            f.write(content)
        with open(tmp_file_path, 'rb') as f:
            try:
                # self.dbx.files_upload(f.read(), '/Apps/Commands/' + file_name, mode=dropbox.files.WriteMode.overwrite)
                self.dbx.files_upload(f.read(), '/Apps/Commands/' + file_name)
                print(f"{file_name} uploaded successfully to Dropbox.")
            except dropbox.exceptions.ApiError as e:
                error_message = f"Failed to upload {file_name} to Dropbox\nDetails:\n{e}"
                print(error_message)
                raise Exception(error_message)
