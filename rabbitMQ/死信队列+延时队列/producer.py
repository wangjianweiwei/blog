# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/2/21 4:43 下午
"""
import pika

# 连接凭证
credentials = pika.PlainCredentials("admin", "admin")
# 连接参数
parameters = pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials, virtual_host="/")
# 建立连接
connection = pika.BlockingConnection(parameters)
# 创建channel
channel = connection.channel()
# 创建正常的交换机和队列
channel.exchange_declare("test_exchange")

# 正常队列绑定死信交换机
# 设置两个参数x-dead-letter-exchange和x-dead-letter-routing-key
arguments = {"x-dead-letter-exchange": "test_exchange_dlx", "x-dead-letter-routing-key": "test_key_dlx",
             "x-message-ttl": 10000}
channel.queue_declare("test_queue", arguments=arguments)
# 队列和交换机进行绑定
channel.queue_bind("test_queue", "test_exchange", routing_key="test_key")

# 创建死信交换机和队列
channel.exchange_declare("test_exchange_dlx")
channel.queue_declare("test_queue_dlx")
# 队列和交换机进行绑定
channel.queue_bind("test_queue_dlx", "test_exchange_dlx", routing_key="test_key_dlx")

channel.basic_publish("test_exchange", routing_key="test_key", body=b'abcdasdasd')
