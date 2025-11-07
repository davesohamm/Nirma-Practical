from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(5):
    message = f"DLQ Test by Soham, Dev, Harsh, Nikhil, Vishwas {i}".encode('utf-8')
    producer.send('main_topic', message)
    print(f"Sent: {message}")

producer.flush()
producer.close()
