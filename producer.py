import pika, json, os

from dotenv import load_dotenv
load_dotenv()
params = pika.URLParameters(os.environ.get('RABBITMQ_CONNECT_URL'))


connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method,body):
    properties = pika.BasicProperties(method)
    body = json.dumps(body)
    channel.basic_publish(exchange='',routing_key='admin',body=body,properties=properties)