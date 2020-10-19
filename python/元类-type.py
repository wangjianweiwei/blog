# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2020/10/19 10:44 下午
"""


class Student(object):
    pass


# 使用type动态定义类
Person = type("Person", (), {})

# 创建出的出现的一样的, class关键字的递增也是调用的type元类
print(Person())
print(Student())

# 添加属性(类属性)
Person1 = type("Person1", (), {"name": None, "age": 18})
print(Person1().age)


# 添加方法
def pay(self):
    print("Pay")


Person2 = type("Person2", (), {"name": None, "age": 18, "pay": pay})
print(Person2().pay())


# 添加静态方法, 类方法
def work(self):
    print(f"work {self}")


@classmethod
def pay(cls):
    print(f"pay {cls}")


@staticmethod
def eat():
    print("eat")


Person3 = type("Person3", (), {"name": None, "age": 18, "pay": pay, "work": work, "eat": eat})
person3 = Person3()
person3.pay()
person3.work()
person3.eat()


# 定义继承

class Person4(object):
    def pay(self):
        print(f"Person4 pay {self}")


class Person5(object):
    def pay(self):
        print(f"Person5 pay {self}")


Person6 = type("Person6", (Person4, Person5))

person6 = Person6()
person6.pay()
