# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2021/3/13 10:00 下午
"""
from abc import ABC, abstractmethod
from collections import namedtuple


class Item:
    def __init__(self, issue, price, quantity):
        self.issue = issue
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity


class Order:
    def __init__(self, customer, promotion=None):
        self.cart = []
        self.customer = customer
        self.promotion = promotion

    def add_to_cart(self, *items):
        for item in items:
            self.cart.append(item)

    def total(self):
        total = 0
        for item in self.cart:
            total += item.total()

        return total

    def due(self):
        if not self.promotion:
            discount = 0
        else:
            discount = self.promotion.discount(self)

        return self.total() - discount


class Promotion(ABC):
    """促销基类"""

    @abstractmethod
    def discount(self, order):
        pass


class FidelityPromo(Promotion):
    """如果积分满1000, 既可以兑换10元代金券"""

    def discount(self, order: Order):
        if order.customer.fidelity > 1000:
            return 10

        return 0


if __name__ == '__main__':
    Customer = namedtuple("Customer", "name fidelity")
    xm = Customer("小明", 1500)
    item1 = Item("鞋子", 200, 3)
    item2 = Item("衣服", 600, 1)
    o = Order(xm, FidelityPromo())
    o.add_to_cart(item1, item2)
    print(o.due())
