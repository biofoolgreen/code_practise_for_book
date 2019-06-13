'''
@Description: python面向对象编程-chap8-设计模式
@Version: 
@Author: liguoying
@Date: 2019-06-06 16:19:52
'''

##################################
####         观察者模式        ####
##################################

class Inventory:
    def __init__(self):
        self.observers = []
        self._product = None
        self._quantity = 0
    
    def attach(self, observer):
        self.observers.append(observer)
    
    @property
    def product(self):
        return self._product
    
    @product.setter
    def product(self, value):
        self._product = value
        # 当更新参数时通知观察者
        self._update_observers()

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        self._update_observers()
    
    def _update_observers(self):
        for observer in self.observers:
            observer()



class ConsoleObeserver:
    """实现一个简单的观察者对象"""
    def __init__(self, inventory):
        self.inventory = inventory
    
    def __call__(self):
        print(self.inventory.product)
        print(self.inventory.quantity)


invent = Inventory()
cons = ConsoleObeserver(invent)
invent.attach(cons)
invent.product = "widget"
invent.quantity = 5