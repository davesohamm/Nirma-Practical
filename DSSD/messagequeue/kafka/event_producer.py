from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

events = [
    {"event": "user_signup", "user": "Soham"},
    {"event": "user_signup", "user": "Dev"},
    {"event": "user_signup", "user": "Harsh"},
    {"event": "user_signup", "user": "Nikhil"},
    {"event": "user_signup", "user": "Vishwas"}
]

for e in events:
    producer.send('event_topic', e)
    print(f"Sent event: {e}")

producer.flush()
producer.close()
