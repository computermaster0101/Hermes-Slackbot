import json
import boto3


class Gatekeeper:
    def __init__(self, keys, is_local=False):
        print('Gatekeeper.__init__')
        self.keys = keys
        self.is_local = is_local

    def is_key_valid(self, api_key):
        print('Gatekeeper.is_key_valid')
        if api_key in self.keys.values():
            return True
        else:
            return False

    def open_the_gate(self, event):
        print('Gatekeeper.open_the_gate')
        event['queryStringParameters']['tmpkey'] = event['queryStringParameters']['apikey']
        event['queryStringParameters']['apikey'] = self.keys['hermes_key']

        if self.is_local:
            return "local"
        else:
            lambda_client = boto3.client('lambda')
            lambda_client.invoke(
                FunctionName='Hermes_Gatekeeper',
                InvocationType='Event',
                Payload=json.dumps(event)
            )

    def close_the_gate(self, event):
        print('Gatekeeper.close_the_gate')
        event['queryStringParameters']['apikey'] = event['queryStringParameters']['tmpkey']
        return event
