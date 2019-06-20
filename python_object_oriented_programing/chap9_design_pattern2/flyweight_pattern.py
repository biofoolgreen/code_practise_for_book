'''
@Description: python面向对象编程-chap9-设计模式2
@Version: 
@Author: liguoying
@Date: 2019-06-20 15:13:24
'''
##################################
####         享元模式          ####
##################################

import weakref

class CarModel:
    # weakref.WeakValueDictionary提供一个弱引用字典方法，
    # 如果字典里的值没有被引用，垃圾收集器将会将其处理
    _models = weakref.WeakValueDictionary()

    def __new__(cls, model_name, *args, **kwargs):
        model = cls._models.get(model_name)
        if not model:
            # 如果不存在则创建
            model = super().__new__(cls)
            cls._models[model_name] = model
        # 存在则直接使用
        return model
    
    def __init__(self, model_name, air=False, tilt=False,
            cruise_control=False, power_lock=False,
            alloy_wheels=False, usb_charger=False):
        if not hasattr(self, 'initted'):
            self.model_name = model_name
            self.air = air
            self.tilt = tilt
            self.cruise_control = cruise_control
            self.power_lock = power_lock
            self.alloy_wheels = alloy_wheels
            self.usb_charger = usb_charger
            self.initted = True
    
    def check_serial(self, serial_number):
        print("""
        Sorry, we are unable to check the serial number {0} on the {1}
        at this time
        """.format(serial_number, self.model_name))
    


class Car:
    """存储附加信息，以及对享元的引用"""
    def __init__(self, model, color, serial):
        self.model = model
        self.color = color
        self.serial = serial
    

    def check_serial(self):
        return self.model.check_serial(self.serial)
    

dx = CarModel("FIT DX")
lx = CarModel("FIT LX", air=True, cruise_control=True, power_lock=True, tilt=True)

car1 = Car(dx, 'blue', "12345")
car2 = Car(dx, 'red', "12346")
car3 = Car(lx, 'black', "12347")


print(id(lx))
del lx
del car3

import gc
print(gc.collect())

lx = CarModel("FIT LX", air=True, cruise_control=True, power_lock=True, tilt=True)
print("before: ", id(lx))
lx = CarModel("FIT LX")
print("after: ", id(lx))
print(lx.air)