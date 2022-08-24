import json
import traceback
import boto3
import requests

HEADER = { 'Content-Type': 'application/json' }
FAILED_FORMAT = '<!here>\n```\n{0}```'
SUCCESS_FORMAT = '{0}が成功しました。'

def lambda_handler(event, context):

    target_queue = 'test.fifo'
    data = {}
    sqs = boto3.resource('sqs')
    
    try:
        queue = sqs.get_queue_by_name(QueueName=target_queue)
        for message in queue.receive_messages():
            
            json_data = json.loads(message.body)
            webhook_url = json_data['webhookUrl']
            text = json_data['text']
            process_name = json_data['processName']

            if not text:
                data = {
                    'text': SUCCESS_FORMAT.format(process_name)
                }
            else: 
                data = {
                    'text': FAILED_FORMAT.format(text)
                }

            response = requests.post(webhook_url, data=json.dumps(data), headers=HEADER)

            message.delete()
    except Exception as e:
        print(traceback.format_exc())
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
