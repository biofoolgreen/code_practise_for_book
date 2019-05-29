'''
@Description: python面向对象编程-chap6-python数据结构
@Version: 
@Author: liguoying
@Date: 2019-05-29 10:31:46
'''

##################################
####       namedtuple         ####
##################################

# from collections import namedtuple

# Stock = namedtuple("Stockq", "symbol current high low")
# s = Stock("GOOG", 612.2, high=615, low=610)

# print(s, s.high)




##################################
####       dictionary         ####
##################################
# from collections import defaultdict
# num_items = 0
# def tuple_counter():
#     global num_items
#     num_items += 1
#     return (num_items, [])

# d = defaultdict(tuple_counter)
# print(d)
# d['a'][1].append("hello")
# d['b'][1].append("world")
# print(d)


##################################
####          list            ####
##################################
# import string
# chrs = list(string.ascii_letters) + [" "]

# def chrs_freq(sentence):
#     freq = [(c, 0) for c in chrs]
#     for letter in sentence:
#         idx = chrs.index(letter)
#         freq[idx] = (letter, freq[idx][1]+1)
#     return freq

# sent = "the quick brown fox jumps over the lazy dog"
# print(chrs_freq(sent))


class WeirdSortee:
    def __init__(self, string, number, sort_num):
        self.string = string
        self.number = number
        self.sort_num = sort_num

    def __lt__(self, object):
        if self.sort_num:
            return self.number < object.number
        return self.string < object.string

    def __repr__(self):
        return f"{self.string}:{self.number}"

a = WeirdSortee('a', 4, True)
b = WeirdSortee('b', 3, True)
c = WeirdSortee('c', 2, True)
d = WeirdSortee('d', 1, True)

l = [a, b, c, d]
print(l)
print(l.sort())
print(l)