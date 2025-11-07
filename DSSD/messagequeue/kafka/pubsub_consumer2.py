from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'broadcast_topic',
    bootstrap_servers='localhost:9092',
    group_id='group2',
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"Consumer 2 received: {message.value.decode('utf-8')}")
