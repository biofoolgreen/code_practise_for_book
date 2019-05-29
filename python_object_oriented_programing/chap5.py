'''
@Description: python面向对象编程-chap5-何时使用面向对象编程
@Version: 
@Author: liguoying
@Date: 2019-05-28 10:23:52
'''

##################################
####         property         ####
##################################

# class Color:
#     def __init__(self, rgb, name):
#         self.rgb = rgb
#         self._name = name
    
#     def _set_name(self, name):
#         if not name:
#             raise Exception("Invalid name")
#         self._name = name
    
#     def _get_name(self):
#         return self._name
    
#     name = property(_get_name, _set_name)

# c = Color("##00ff", 'bright red')
# print(c.name)
# c.name = 'red'
# print(c.name)
# c.name = ''



# class Foo:
#     def __init__(self, foo):
#         self._foo = foo
    
#     @property
#     def foo(self):
#         return self._foo
    
#     @foo.setter     # 当foo被property修饰后，自动获得setter方法，用于修饰其他函数
#     def foo(self, value):
#         self._foo = value



# from urllib.request import urlopen
# import time

# class WebPage:
#     def __init__(self, url):
#         self.url = url
#         self._content = None
    
#     @property
#     def content(self):
#         if not self._content:
#             print("Retrieving new page")
#             self._content = urlopen(self.url).read()
#         return self._content
# wp = WebPage("www.baidu.com")
# now1 = time.time()
# cont1 = wp.content
# print("first time:", time.time() - now1)
# now2 = time.time()
# cont2 = wp.content
# print("second time(use local cache): ", time.time() - now2)


##################################
####         管理对象          ####
##################################
# import sys
# import os
# import shutil
# import zipfile
# from pathlib import Path

# class ZipReplace:
#     """对zip文件中的文件进行查找替换并重新压缩"""
#     def __init__(self, filename, search_str, replace_str):
#         self.filename = filename
#         self.search_str = search_str
#         self.replace_str = replace_str
#         self.tmp_dict = Path(f"unzipped-{filename}")
    
#     def zip_find_replace(self):
#         self.unzip_files()
#         self.find_replace()
#         self.zip_files()
    
#     def unzip_files(self):
#         os.mkdir(self.tmp_dict)
#         zipf = zipfile.ZipFile(self.filename)
#         try:
#             zipf.extractall(self.tmp_dict)
#         finally:
#             zipf.close()
    
#     def find_replace(self):
#         for filename in self.tmp_dict.iterdir():
#             with filename.open() as file:
#                 contents = file.read()
#                 contents = contents.replace(self.search_str, self.replace_str)
#             with filename.open("w") as file:
#                 file.write(contents)
    
#     def zip_files(self):
#         with zipfile.ZipFile(self.filename, "w") as file:
#             for filename in self.tmp_dict.iterdir():
#                 file.write(filename, filename.name)
#         shutil.rmtree(self.tmp_dict)


# if __name__ == "__main__":
#     ZipReplace(*sys.argv[1:4]).zip_find_replace()


##################################
####       Case Study         ####
##################################

class Document:
    def __init__(self):
        self.chracters = []
        # self.cursor = 0
        self.cursor = Cursor(self)
        self.filename = ''
    

    def insert(self, chracter):
        if not hasattr(chracter, 'chracter'):
            chracter = Chracter(chracter)
        # self.chracters.insert(self.cursor, chracter)
        self.chracters.insert(self.cursor.position, chracter)
        # self.cursor += 1
        self.cursor.forward()
    
    def delete(self):
        # del self.chracters[self.cursor]
        del self.chracters[self.cursor.position]
    
    def save(self):
        with open(self.filename, 'w') as f:
            f.write(''.join(self.chracters))
    
    # def forward(self):
    #     self.cursor += 1
    
    # def back(self):
    #     self.cursor -= 1

    @property
    def string(self):
        # return ''.join(self.chracters)
        return "".join(str(c) for c in self.chracters)



class Cursor:
    def __init__(self, document):
        self.document = document
        self.position = 0

    def forward(self):
        self.position += 1
    
    def back(self):
        self.position -= 1     
    
    def home(self):
        # while self.document.chracters[self.position-1] != '\n':
        while self.document.chracters[self.position-1].chracter != '\n':
            self.position -= 1
            if self.position == 0:
                break
    
    def end(self):
        # while (self.position < len(self.document.chracters) and
        #         self.document.chracters[self.position] != '\n'):
        while (self.position < len(self.document.chracters) and
                self.document.chracters[self.position].chracter != '\n'):
            self.position += 1


class Chracter:
    def __init__(self, chracter, bold=False, italic=False, underline=False):
        assert len(chracter) == 1
        self.chracter = chracter
        self.bold = bold
        self.italic = italic
        self.underline = underline
    
    def __str__(self):
        bold = "*" if self.bold else ""
        italic = "/" if self.italic else ""
        underline = "_" if self.underline else ""
        return bold + italic + underline + self.chracter
