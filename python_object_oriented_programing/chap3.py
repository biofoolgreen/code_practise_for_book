'''
@Description: python面向对象编程-chap3
@Version: 
@Author: liguoying
@Date: 2019-05-22 10:23:51
'''

# class ContactList(list):
#     def search(self, name):
#         """Return all contacts that contain the search value in their name."""
#         matched = []
#         # 这里的self指代的是list类本身
#         for contact in self:
#             print("ContactList search method `self` for : ", self)
#             if name in contact.name:
#                 matched.append(contact)
#         return matched


# class Contact:

#     all_contacts = ContactList()

#     def __init__(self, name, email):
#         self.name = name
#         self.email = email
#         # Contact.all_contacts.append(self)
#         self.all_contacts.append(self)


# class Friend(Contact):
#     def __init__(self, name, email, phone):
#         super().__init__(name, email)
#         # super().__init__(*args, **kwargs)
#         self.phone = phone

# class Supplier(Contact):

#     def order(self, order):
#         print("If this were a real system we would send {} order to {}".format(order, self.name))



# a = Contact('Alice', "alice@xxx.com")
# # print(a.all_contacts)
# # print(Contact.all_contacts)
# b = Contact('Bob', "bob@yyy.com")
# b1 = Contact('Bob copy', "bob1@yyy.com")
# b2 = Contact('Bob reverse', "bob2@yyy.com")

# bname = [bn.name for bn in Contact.all_contacts.search('Bob')]
# print(bname)
# # print(b.all_contacts)
# # print(Contact.all_contacts)

# c = Supplier('Charlie', "charlie@zzz.com")
# c.order("12345")
# # print(c.all_contacts)


################################################
##              钻石继承问题                   ##
################################################

# class BaseClass:
#     num_base_call = 0
#     def call_me(self):
#         print("Calling method on Base Class")
#         self.num_base_call += 1


# class LeftSubClass(BaseClass):
#     num_left_call = 0
#     def call_me(self):
#         # BaseClass.call_me(self)
#         super().call_me()
#         print("Calling method on Left SubClass")
#         self.num_left_call += 1


# class RightSubClass(BaseClass):
#     num_right_call = 0
#     def call_me(self):
#         # BaseClass.call_me(self)
#         super().call_me()
#         print("Calling method on Right SubClass")
#         self.num_right_call += 1


# class SubClass(LeftSubClass, RightSubClass):
#     num_sub_call = 0
#     def call_me(self):
#         # LeftSubClass.call_me(self)
#         # RightSubClass.call_me(self)
#         super().call_me()
#         print("Calling method on SubClass")
#         self.num_sub_call += 1

# s = SubClass()

# s.call_me()
# # BaseClass的call_me方法被调用了两次
# print(s.num_base_call, s.num_left_call, s.num_right_call, s.num_sub_call)


################################################
##              使用不同的参数                 ##
################################################

# class Contact:
#     all_contacts = []
#     def __init__(self, name="", email="", **kwargs):
#         super().__init__(**kwargs)
#         self.name = name
#         self.email = email
#         self.all_contacts.append(self)


# class AddressHolder:
#     def __init__(self, street="", city="", state="", code="", **kwargs):
#         super().__init__(**kwargs)
#         self.street = street
#         self.city = city
#         self.state = state
#         self.code = code


# class Friend(Contact, AddressHolder):
#     def __init__(self, phone="", **kwargs):
#         super().__init__(**kwargs)
#         self.phone = phone



################################################
##               多态                         ##
################################################

class AudioFile:
    def __init__(self, filename):
        if not filename.endswith(self.ext):
            raise Exception("Invalid File format")
        
        self.filename = filename


class MP3File(AudioFile):
    ext = 'mp3'
    def play(self):
        print("Playing {} as mp3".format(self.filename))


class WAVFile(AudioFile):
    ext = 'wav'
    def play(self):
        print("Playing {} as wav".format(self.filename))


class OGGFile(AudioFile):
    ext = 'ogg'
    def play(self):
        print("Playing {} as ogg".format(self.filename))


ogg = OGGFile("audio.ogg")
mp3 = MP3File('audio.mp3')
ogg.play()
mp3.play()
ad = AudioFile('hh.wav')
ad.play()