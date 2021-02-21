# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/2/21 9:16 上午
"""
import pika

# 连接凭证
credentials = pika.PlainCredentials("admin", "admin")
# 连接参数
parameters = pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials)
# 建立连接
connection = pika.BlockingConnection(parameters)
# 创建channel
channel = connection.channel()
# 创建队列
queue = "work_queues"
# 已经存在的队列不会重复创建(但要保证队列的参数一直)
channel.queue_declare(queue=queue)
"""
参数:
    queue: 队列名称
    passive=False,
    durable=False: 是否持久化
    exclusive=False: 只允许当前的链接访问
    auto_delete=False: 断开链接后是否自动删除
    arguments=None: 队列的自定义键/值参数
"""
# 发布消息
while True:
    message = input("请输入要发布的消息: ").strip()
    if message.upper() == "Q":
        break

    channel.basic_publish(exchange="", routing_key=queue, body=message.encode("UTF-8"))
    """
    参数:
        exchange: 使用的交换机名称(空字符串代表使用默认的交换机)
        routing_key: 在当前的模式下, 表示队列的名称
        body: 要发送的消息(byte类型)
        properties=None: 消息属性
        mandatory=False: 强制性标记
    """
    print("消息发送成功...")

connection.close()
