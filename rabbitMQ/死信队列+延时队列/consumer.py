# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/2/21 9:16 上午
"""
import os
import sys
import time
import pika


def main():
    # 连接凭证
    credentials = pika.PlainCredentials("admin", "admin")
    # 连接参数
    parameters = pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials)
    # 建立连接
    connection = pika.BlockingConnection(parameters)
    # 创建channel
    channel = connection.channel()
    # 创建队列
    queue = channel.queue_declare(queue="", exclusive=True)
    # 创建交换机
    exchange = "test_exchange"
    channel.exchange_declare(exchange, exchange_type="direct")
    # 将队列绑定到交换机上, 并指定routing_key
    channel.queue_bind(queue=queue.method.queue, exchange=exchange, routing_key="test")

    # 消费消息
    def callback(_channel, method, properties, body):
        print(f"接受到消息: {body.decode('UTF-8')}")

    channel.basic_consume(queue=queue.method.queue, on_message_callback=callback, auto_ack=True)
    # 对个worker之间是竞争关系
    """
    参数:
    queue: 指定消费的队列名称
    on_message_callback: 接受到消息后的回调
    auto_ack=False: 是否自动确认
    exclusive=False: 不允许其他消费者使用这个队列
    consumer_tag=None,
    arguments=None
    """

    # 开始消费
    channel.start_consuming()


if __name__ == '__main__':
    try:
        print("start......")
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
