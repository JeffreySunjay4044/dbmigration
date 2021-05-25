import os
from typing import Dict

from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
from query_process import msg_processor


def build_consumer() -> Dict:
    return {
        'bootstrap.servers': os.getenv("BOOTSTRAP_SERVER"),
        'group.id': os.getenv("GROUP_ID"),
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
    }


def start_consumer() -> None:
    topics = ["dbhistory.mercatoaltertest"]
    is_ddl = True
    c = Consumer(build_consumer())
    c.subscribe(topics)
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_processor.process_message(msg, is_ddl)
    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')
    c.close()
