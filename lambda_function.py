import re
import json
import base64
from urllib.parse import parse_qs
from datetime import datetime
from upload_file import FileUploader

api_token = ""
dropbox_access_token = ""


def lambda_handler(event, context):
    print('An event occurred!')
    print(event)
    try:
        api_key = event['queryStringParameters']['apikey']
        if api_key == api_token:
            print('The api token has been validated!')
            body = base64.b64decode(event['body']).decode('utf-8')
            parsed_body = parse_qs(body)
            text = parsed_body['text'][0]
            match = re.match(r'system\s*(\d+)\s*(.*)', text)
            if match:
                device = f'system{match.group(1)}'
                message = match.group(2)
                timestamp = datetime.now().strftime('%B %d, %Y at %I:%M%p')
                file_name = f'{device}.txt'
                upload_file = FileUploader(dropbox_access_token=dropbox_access_token)
                upload_file.dropbox(file_name, json.dumps({
                    'device': device,
                    'message': message,
                    'timestamp': timestamp
                }))
                return {
                    'statusCode': 202,
                    'Content-type': 'application/json',
                    'body': json.dumps('Hello from Lambda!') + "\nI got your message!\n" + text
                }
            else:
                print('The pattern did not match!')
                return {
                    'statusCode': 400,
                    'body': 'bad request'
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
