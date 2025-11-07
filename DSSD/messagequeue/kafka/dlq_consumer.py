from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer(
    'main_topic',
    bootstrap_servers='localhost:9092',
    group_id='dlq_group',
    auto_offset_reset='earliest'
)

dlq_producer = KafkaProducer(bootstrap_servers='localhost:9092')

for message in consumer:
    msg = message.value.decode('utf-8')
    try:
        if "3" in msg:  # simulate processing error
            raise ValueError("Simulated error")
        print(f"Processed: {msg}")
    except Exception as e:
        print(f"Error processing {msg}: {e}")
        dlq_producer.send('dlq_topic', msg.encode('utf-8'))

dlq_producer.flush()
dlq_producer.close()
