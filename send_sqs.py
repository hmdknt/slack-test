import json
import traceback
import boto3

WEBHOOK_URL = ''
PROCESS_NAME = 'TestFunc'

def lambda_handler(event, context):

    target_queue = 'test.fifo'
    data = {}
    sqs = boto3.resource('sqs')

    try:
        queue = sqs.get_queue_by_name(QueueName=target_queue)
        data = {
            "webhookUrl": WEBHOOK_URL,
            "text": "",
            "processName": PROCESS_NAME
        }
    except Exception as e:
        message = str(traceback.format_exc())
        data = {
            "webhookUrl": WEBHOOK_URL,
            "text": message,
            "processName": PROCESS_NAME
        }

    response = queue.send_message(MessageGroupId='group1', MessageBody=json.dumps(data))
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
