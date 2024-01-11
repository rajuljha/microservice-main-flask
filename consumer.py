import pika, json, os

from main import Product, db
from dotenv import load_dotenv
load_dotenv()

params = pika.URLParameters(os.environ['RABBITMQ_CONNECT_URL'])

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print(" [x] Received in main")
    if body is not None:
        data = json.loads(body)
        print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'],title=data['title'],image=data['image'])
        db.session.add(product)
        db.session.commit()
        print(" [x] Product created")

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print(" [x] Product updated")

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print(" [x] Product deleted")

channel.basic_consume(queue='main',on_message_callback=callback,auto_ack=True)
print(' [*] Started consuming')
channel.start_consuming()

channel.close()