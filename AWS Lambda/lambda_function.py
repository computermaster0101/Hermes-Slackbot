import json
import boto3

from hermes_gatekeeper import HermesGatekeeper

my_config_file = 'config_file.json'


def lambda_handler(event, context):
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

    gatekeeper = HermesGatekeeper(my_config_file)
    gatekeeper.response.append('Hello from The Gatekeeper!')
    if not event.get('headers').get('x-slack-retry-num') is None:
        gatekeeper.response.append('You sent a duplicate message!')
        print('returning status 200 to slackbot retry attempt')
        return {'statusCode':200}

    # try:
    if gatekeeper.is_key_valid(event['queryStringParameters']['apikey']):
        gatekeeper.response.append('The api token has been validated!')

        if event['queryStringParameters']['apikey'] == gatekeeper.tokens['hermes_relay_key']:
            gatekeeper.response.append('Welcome Hermes!')
            hermes_dispatch(event)

        elif event['queryStringParameters']['apikey'] == gatekeeper.tokens['slack_at_api_key']:
            gatekeeper.response.append('Welcome Slackbot Commander!')
            open_the_gate(gatekeeper, event)
            print('sending 200')
            return {'statusCode': 200}

        elif event['queryStringParameters']['apikey'] == gatekeeper.tokens['slack_slash_api_key']:
            gatekeeper.response.append('Welcome Slackbot Slasher!')
            open_the_gate(gatekeeper, event)
            output = gatekeeper.get_output_string()
            print('sending 200')
            return {'statusCode': 200, 'body': f'OK {output}'}

        elif event['queryStringParameters']['apikey'] == gatekeeper.tokens['dialogflow_api_key']:
            gatekeeper.response.append('Welcome Dialogflow!')
            gatekeeper.response.append('This has not been implimented')
            output = gatekeeper.get_output_string()
            return {'statusCode': 202, 'body': f'{output}'}

        else:
            gatekeeper.response.append('The key is invalid!')
            gatekeeper.send_message()
            output = gatekeeper.get_output_string()
            return {'statusCode': 403, 'body': f'forbidden\n{output}'}
"""
    except Exception as e:
        print('Unidentified internal server error!')
        print(e)
        return {
            'statusCode': 500,
            'body': 'internal server error'
        }
"""

def open_the_gate(gatekeeper, event):
    event['queryStringParameters']['tmpkey'] = event['queryStringParameters']['apikey']
    event['queryStringParameters']['apikey'] = gatekeeper.tokens['hermes_relay_key']
    gatekeeper.send_message()
    output = gatekeeper.get_output_string()

    lambda_client = boto3.client('lambda')
    lambda_client.invoke(
        FunctionName='Hermes_Gatekeeper',
        InvocationType='Event',
        Payload=json.dumps(event)
    )


def hermes_dispatch(event):
    event['queryStringParameters']['apikey'] = event['queryStringParameters']['tmpkey']
    hermes = HermesGatekeeper(my_config_file)
    hermes.get_data_from_event(event)
    if hermes.is_pattern_valid():
        hermes.get_message_object()
        try:
            hermes.file_upload()
            hermes.response.append(f'Your message is being promptly delivered!\n{json.dumps(hermes.message_object)}')
            hermes.send_message()
            output = hermes.get_output_string()
            return {
                'statusCode': 200,
                'body': f'{output}'
            }
        except Exception as e:
            hermes.response.append('An internal server error occurred:\n' + str(e))
            hermes.send_message()
            output = hermes.get_output_string()
            return {
                'statusCode': 200,
                'body': f'{output}'
            }
    else:
        hermes.response.append(f'The pattern did not match!\ninvalid command:\n{hermes.text}')
        hermes.send_message()
        output = hermes.get_output_string()
        return {
            'statusCode': 200,
            'body': f'{output}'
        }
