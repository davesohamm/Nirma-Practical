from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(10):
    message = f"Multiple consumers in the same consumer group share tasks/messages. We are : Soham, Dev, Harsh, Nikhil, Vishwas  {i}".encode('utf-8')
    producer.send('workqueue_topic', message)
    print(f"Sent: {message}")

producer.flush()
producer.close()
