from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'ptp_topic',
    bootstrap_servers='localhost:9092',
    group_id='ptp_group',   # ensures only one consumer in group gets a message
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"Received: {message.value.decode('utf-8')}")
