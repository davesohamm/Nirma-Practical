from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(5):
    message = f"Soham sent broadcast, Dev sent broadcast, Harsh sent broadcast, Nikhil sent broadcast, Vishwas sent broadcast {i}".encode('utf-8')
    producer.send('broadcast_topic', message)
    print(f"Sent: {message}")

producer.flush()
producer.close()
