'''
@Description: python面向对象编程-chap8-设计模式
@Version: 
@Author: liguoying
@Date: 2019-06-06 16:19:52
'''

##################################
####          策略模式         ####
##################################
from PIL import Image

class TiledStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file)
        out_img = Image.new("RGB", desktop_size)
        num_tiles = [o // i + 1 for o, i in zip(out_img.size, in_img.size)]
        for x in range(num_tiles[0]):
            for y in range(num_tiles[1]):
                out_img.paste(in_img, ( in_img.size[0] * x,
                                        in_img.size[1] * y,
                                        in_img.size[0] * (x + 1),
                                        in_img.size[1] * (y + 1),),)
        return out_img


class CenteredStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file)
        out_img = Image.new("RGB", desktop_size)
        left = (out_img.size[0] - in_img.size[0]) // 2
        top = (out_img.size[1] - in_img.size[1]) // 2
        out_img.paste(in_img, (left, top, left + in_img.size[0], top + in_img.size[1]),)
        return out_img


class ScaledStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file)
        out_img = in_img.resize(desktop_size)
        return out_img