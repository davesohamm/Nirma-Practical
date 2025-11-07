from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(10):
    message = f"Hello This is Nirma MTech DS Lab Practical for DSSD : Our group is Soham, Dev, Harsh, Nikhil, Vishwas. {i}".encode('utf-8')
    producer.send('ptp_topic', message)
    print(f"Sent: {message}")

producer.flush()
producer.close()
