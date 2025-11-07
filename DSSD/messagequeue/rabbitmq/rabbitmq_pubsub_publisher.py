import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# Create a fanout exchange named 'logs' for broadcasting
channel.exchange_declare(exchange='logs', exchange_type='fanout')
message = 'Broadcast: Hello subscribers! This is us : Soham, Dev, Harsh, Nikhil and Vishwas! Nirma MTech DS Practical...'
channel.basic_publish(exchange='logs', routing_key='', body=message)
print('[x] Sent broadcast')
connection.close()
