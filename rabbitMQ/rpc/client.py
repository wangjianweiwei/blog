# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/2/21 2:59 下午
"""
import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        credentials = pika.PlainCredentials("admin", "admin")
        parameters = pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        body = str(n).encode("UTF-8")
        properties = pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id)
        self.channel.basic_publish(exchange='', routing_key='rpc_queue', properties=properties, body=body)

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
