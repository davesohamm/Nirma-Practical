import pika
import sys
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# Declare queue 'task_queue' as durable so messages survive RabbitMQ restarts
channel.queue_declare(queue='task_queue', durable=True)
message = ' '.join(sys.argv[1:]) or 'Hello Nirma MTech DS! We are : Soham, Dev, Harsh, Nikhil and Vishwas! We performed this practical in group...'
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
)
print("[x] Sent:\n", message)
connection.close()
