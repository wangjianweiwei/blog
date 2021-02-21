# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/2/21 2:59 下午
"""
import pika

credentials = pika.PlainCredentials(username="admin", password="admin")
parameters = pika.ConnectionParameters(host="", credentials=credentials, virtual_host="/")
connect = pika.BlockingConnection(parameters=parameters)
channel = connect.channel()

channel.queue_declare("rpc_queue")


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

channel.start_consuming()
