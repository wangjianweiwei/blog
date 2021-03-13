# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/3/13 10:51 下午
Django中信号的简单版
"""


class Signal:
    def __init__(self, name: str):
        self.receivers = []
        self.name = name

    @staticmethod
    def make_id(target):
        return id(target)

    def connect(self, receiver, sender=None, **kwargs):
        self.receivers.append(((self.make_id(receiver), self.make_id(sender)), receiver))

    def send(self, sender, **kwargs):
        _sender_key = self.make_id(sender)
        for (receiver_key, sender_key), receiver in self.receivers:
            if sender_key == _sender_key:
                receiver(self, sender, **kwargs)

    def __str__(self):
        return f"<{self.__class__.__name__} {self.name}>"


def receiver(signal, **kwargs):
    def _decorator(func):
        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(func, **kwargs)
        else:
            signal.connect(func, **kwargs)
        return func

    return _decorator


if __name__ == '__main__':
    log = Signal("log")


    class A:
        pass


    class B:
        pass


    @receiver(log, sender=A)
    def console(signal, sender, **kwargs):
        print("console", signal, sender, kwargs)


    @receiver(log, sender=B)
    def file(signal, sender, **kwargs):
        print("file", signal, sender, kwargs)


    @receiver(log, sender=B)
    def file(signal, sender, **kwargs):
        print("db", signal, sender, kwargs)


    log.send(sender=B, a=10, b=[1, 2, 3])
