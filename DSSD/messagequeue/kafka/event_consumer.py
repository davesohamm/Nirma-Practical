from kafka import KafkaConsumer
import json

# Create a Kafka consumer
consumer = KafkaConsumer(
    'event_topic',
    bootstrap_servers='localhost:9092',
    group_id='event_group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest'
)

# Consume messages
for record in consumer:
    # record is a ConsumerRecord object
    event = record.value  # Extract the actual dictionary
    print(f"Received event: {event}")
    
    # Process the event
    if event['event'] == 'user_signup':
        print(f"Triggering welcome email to {event['user']}")
