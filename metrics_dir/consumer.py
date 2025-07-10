#!/usr/bin/env python
import pika, sys, os
import json
from time import sleep
import requests

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='metrics')
    channel.queue_purge(queue='metrics')
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(json.dumps(data, indent=2))

        res = requests.post(
                "http://127.0.0.1:8001/receive", 
                headers={"Content-Type": "application/json"}, 
                data=json.dumps(data)
        )
        print(json.dumps(data, indent=2))
        
        sys.stdout.flush()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='metrics', on_message_callback=callback, auto_ack=False)
    
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)