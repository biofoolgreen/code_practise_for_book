'''
@Description: python面向对象编程-chap8-设计模式
@Version: 
@Author: liguoying
@Date: 2019-06-11 15:01:38
'''
##################################
####          单例模式         ####
##################################

class OneOnly:
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(OneOnly, cls).__new__(cls, *args, **kwargs)
        return cls._singleton


o1 = OneOnly()
o2 = OneOnly()
print(o1, o2, o1==o2)