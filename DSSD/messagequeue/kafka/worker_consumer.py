from kafka import KafkaConsumer
import time

consumer = KafkaConsumer(
    'workqueue_topic',
    bootstrap_servers='localhost:9092',
    group_id='workers_group',  # all workers share tasks
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"Worker got: {message.value.decode('utf-8')}")
    time.sleep(1)  # simulate task processing
