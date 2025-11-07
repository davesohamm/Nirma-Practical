from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'broadcast_topic',
    bootstrap_servers='localhost:9092',
    group_id='group1',  # different group for each subscriber
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"Consumer 1 received: {message.value.decode('utf-8')}")
