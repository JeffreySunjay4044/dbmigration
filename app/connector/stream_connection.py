import os
from typing import Dict

from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
from query_process import msg_processor


# Consumer configuration
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md



def build_consumer() -> Dict:
    """
    Parse arguments and return connection info for Redshift
    """
    return  {
        'bootstrap.servers': os.getenv("BOOTSTRAP_SERVER"),
        'group.id': os.getenv("GROUP_ID"),
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
    }

def start_consumer():
    # conf = {
    #     'bootstrap.servers': 'localhost:9092',
    #     'group.id': "mercato_test",
    #     'session.timeout.ms': 6000,
    #     'default.topic.config': {'auto.offset.reset': 'smallest'},
    # # 'security.protocol': 'SSL',
    # # 'sasl.mechanisms': 'SCRAM-SHA-256',
    # # 'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
    # # 'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
    # }
    topics = ["dbhistory.inventory"]
    is_ddl = True
    c = Consumer(build_consumer())
    c.subscribe(topics)
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            print(f"message is {msg}")
            if msg.error():
                # Error or event
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    # Error
                    raise KafkaException(msg.error())
            else:
                # Proper message
                msg_processor.process_message(msg, is_ddl)
    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')
    # Close down consumer to commit final offsets.
    c.close()




