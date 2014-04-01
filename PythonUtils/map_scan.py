# coding: utf-8

from FileWriter import FileWriter
from collect_pics import write_collect_bits
import Image
import argparse
import os
import sys


class vector2:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        
    def getX(self):
        return self._x
    x = property(fget=getX)
    
    def getY(self):
        return self._y
    y = property(fget=getY)
    
    def setX(self, x):
        self._x = x
        
    def setY(self, y):
        self._y = y
        
    def __str__(self):
        return "vector2(" + str(self._x) + " " + str(self._y) + ")"
    
class Rect():
    '''
        每个二维空间插入元素的位置和长宽结构
        
        (x0, y0) ------------
            |               |
            |               |
            |               |
            -------------(x1, y1)
    '''
    def __init__(self, area):
        '''
        
        @param area: (x0, y0, x1, y1)
        '''
        self.x0 = area[0]
        self.y0 = area[1]
        self.x1 = area[2]
        self.y1 = area[3]
        
    '''
        使用property映射函数到参数
    '''

    def get_width(self):
        return self.x1 - self.x0
    width = property(fget=get_width)

    def get_height(self):
        return self.y1 - self.y0
    height = property(fget=get_height)
    
    def get_x(self):
        return self.x0
    x = property(fget=get_x)
    
    def get_y(self):
        return  self.y0
    y = property(fget=get_y)
    
    def get_rect(self):
        '''
        获取一个数组形式的区域描述
        '''
        return (self.x0, self.y0, self.x1, self.y1)
    
    def intersects(self, rect):
        '''
            矩形相互交叉测试
        '''
        if (self.x0 >= rect.x1) or (self.x1 <= rect.x0):
            return False
        elif (self.y0 >= rect.y1) or (self.y1 <= self.y0):
            return False
        
        return True
    
    def set_x(self, x):
        width = self.get_width()
        
        self.x0 = x
        
        self.x1 = self.x0 + width
        
    def set_y(self, y):
        height = self.get_height()
        
        self.y0 = y
        
        self.y1 = self.y0 + height
        
    def set_width(self, w):
        self.x1 = self.x0 + w
        
    def set_height(self, h):
        self.y1 = self.y0 + h
    
    def __str__(self):
        return "rect: " + "X: " + str(self.x0) + " Y: " + str(self.y0) + " WH: " + str(self.width) + " " + str(self.height)

def splice_images(collect_images, map_width, map_height):
    """
        拼合图片
    """
    lt = vector2(map_width, map_height)
    rb = vector2(0, 0)
    
    print "需要拼合的图片：" + str(collect_images)
    
    for image_info in collect_images:
        image = Image.open(image_info["image"])
        
        ltx = image_info["x"]
        lty = image_info["y"]
        rbx = ltx + image.size[0]
        rby = lty + image.size[1]
        
        if ltx < lt.x:
            lt.setX(ltx)
        if lty < lt.y:
            lt.setY(lty)
            
        if rbx > rb.x:
            rb.setX(rbx)
        if rby > rb.y:
            rb.setY(rby)
            
    print "拼合图片的左上点: " + str(lt)
    print "拼合图片的右下点: " + str(rb)
            
    collect_image = Image.new("RGBA", (rb.x - lt.x, rb.y - lt.y))
    
    for image_info in collect_images:
        image = Image.open(image_info["image"]).convert("RGBA")
        
        ltx = image_info["x"] - lt.x
        lty = image_info["y"] - lt.y
        
        r, g, b, a = image.split()
        img = Image.merge("RGB", (r, g, b))
        # 使用mask，以使像素混合
        mask = Image.merge("L", (a,))
        
        collect_image.paste(img, (ltx, lty, ltx + image.size[0], lty + image.size[1]), mask)
        
    # debug
#    collect_image.save("test.png")
    
    return collect_image, lt, rb

def read_map(map_path):
    f = open(map_path, "r")
        
    # 去除换行符等
    lines = f.read().splitlines()
    
    map_width = 0;
    map_height = 0;
    
    background_layer, collect_layer, player_layer = range(3)
    curr_layer = -1
    
    left_player_points = []
    right_player_points = []
    collect_images = []
    for line in lines:
        splits = line.split(" ")
        
        key = splits[0]
        
        if key == "canvas":
            map_width = int(splits[1])
            map_height = int(splits[2])
        elif key == "layer":
            if splits[1] == "1":
                curr_layer = collect_layer
            else:
                curr_layer = background_layer
        elif key == "player_layer":
            curr_layer = player_layer
            
        if curr_layer == collect_layer and key == "sprite":
            image = {"image":splits[1], "x":int(splits[3]), "y":int(splits[4])}
            collect_images.append(image)
        elif curr_layer == player_layer and key == "player":
            if splits[1] == "1":
                p = vector2(int(splits[2]), int(splits[3]))
                left_player_points.append(p)
            elif splits[1] == "2":
                p = vector2(int(splits[2]), int(splits[3]))
                right_player_points.append(p)
            
    print collect_images
    print "map: " + str(map_width) + " " + str(map_height)
    return collect_images, map_width, map_height, left_player_points, right_player_points

def scan_map(map_path, resource_dir = None):
    """
        扫描处理指定.map文件
    """
    
    print "scan map: " + map_path
    
    collect_images, map_width, map_height, lp, rp = read_map(map_path)
    
    print collect_images

    if resource_dir != None:
        for image_info in collect_images:
            image_name = image_info["image"]
            
            dir_name = image_name.split("_")[0]
        
            image_path = os.path.join(resource_dir, dir_name, image_name)
        
            image_info["image"] = image_path
        
    print collect_images
    
    collect_image, lt, rb = splice_images(collect_images, map_width, map_height)
    
    out_path = os.path.join(os.path.dirname(map_path), "data")
    if os.path.exists(out_path):
        os.remove(out_path)
    
    out_file = FileWriter(out_path)
    
    # 地图整体长宽
    out_file.WriteInt(map_width)
    out_file.WriteInt(map_height)
    
    # 可破坏区域的长宽，在拼好的图片的图片区域内给出
    rect = Rect((0, 0, collect_image.size[0], collect_image.size[1]))
    if lt.x < 0:
        rect.x0 = -lt.x
    
    if lt.y < 0:
        rect.y0 = -lt.y
        
    if rb.x > map_width:
        rect.x1 = collect_image.size[0] - (rb.x - map_width)
        
    if rb.y > map_height:
        rect.y1 = collect_image.size[1] - (rb.y - map_height)
        
    print "destory rect: " + str(rect)
    print "LT: " + str(lt) + " RB: " + str(rb) + " collect WH: " + str(collect_image.size[0]) + " " + str(collect_image.size[1])

    # 写入破坏区域大小
    out_file.WriteInt(rect.width)
    out_file.WriteInt(rect.height)
    
    # 可破坏区域的坐标信息
    # 给出可破坏区/扫瞄区的左下点相对于整个地图的左下点的定位信息
    if lt.x < 0:
        left = 0;
    else:
        left = lt.x
        
    if rb.y > map_height:
        right = 0
    else:
        right = map_height - rb.y
        
    out_file.WriteInt(left)
    out_file.WriteInt(right)
    
    crop_image = collect_image.crop(rect.get_rect())
#    crop_image.save("out.png")
    
    print crop_image
    
    write_collect_bits(out_file, crop_image, 1)
    
    # 玩家定位数据
    # if len(lp) != 0 or len(rp) != 0:
    #     out_file.WriteInt(1)
    #     
    #     out_file.WriteInt(len(lp))
    #     for p in lp:
    #         out_file.WriteInt(p.x)
    #         out_file.WriteInt(p.y)
    #         
    #     out_file.WriteInt(len(rp))
    #     for p in rp:
    #         out_file.WriteInt(p.x)
    #         out_file.WriteInt(p.y)
    # else:
    #     out_file.WriteInt(0)

    out_file.close()

def main(argv):
    parser = argparse.ArgumentParser(description="scan pictures, get bit information")
    parser.add_argument('-i', '--input', help='input map file', dest="input", default=".")
    parser.add_argument('-r', '--resource', help='resource dir', dest="res", default=None)
    
    args = parser.parse_args()

    map_path = args.input
    res_dir = args.res
    
    if res_dir != None:
        scan_map(map_path)
    else:
        scan_map(map_path, res_dir)

if __name__ == "__main__":
    main(sys.argv[1:])