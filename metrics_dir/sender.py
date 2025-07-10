#!/usr/bin/env python
import pika
import psutil
import json
import sys
from time import sleep

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='metrics')

for _ in range(100):
    metrics = {
    'CPU': psutil.cpu_count(),
    'Virtual Memory': psutil.virtual_memory().total,
    'Used RAM': round(psutil.virtual_memory().percent,2),
    'Memory Left': round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total,2)
    }
    metrics_json = json.dumps(metrics)

    json_object = json.loads(metrics_json)
    json_formatted_str = json.dumps(json_object, indent=2)

    channel.basic_publish(exchange='', routing_key='metrics', body=metrics_json)
    print(" [x] Sent metrics!")
    print(metrics_json)

    sleep(3)
    
    sys.stdout.flush()
    
connection.close()