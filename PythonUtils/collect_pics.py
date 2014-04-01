#coding: utf-8
from FileWriter import FileWriter
import Image
import argparse
import math
import numpy
import os
import struct
import sys

'''
    光栅扫描处理
'''

def get_collect_bits(img, size, min_alpha=1):
    width = img.size[0]
    height = img.size[1]

    img_as_array = numpy.array(img)
    
    alpha = img_as_array[:, :, 3]
    
    # 所有alpha（不透明度）大于min_alpha的都为True
    semi_transparent_indices = (alpha >= min_alpha)

#    print semi_transparent_indices
    
    # 使用一个bool array保存光栅测试结果
    coll_bits = []

    for i in range(0, height, size):
        x_bits = semi_transparent_indices[i : i + size]
        
#        print "Y: " + str(i) + " XL: " + str(x_bits) + " all: " + str(x_bits.all()) + " any: " + str(x_bits.any())
        # TODO: 当一个横向矩阵中所有的值都是True或False时，不做for循环，直接extend
        if x_bits.all():
            for j in range(0, width, size):
                coll_bits.append(True)
        elif not x_bits.any():
            for j in range(0, width, size):
                coll_bits.append(False)
        else:
            for j in range(0, width, size):
                bits = x_bits[:, j : j + size]
                # 有一个为true则取True
                coll_bits.append(bits.any())

#    print " Longth: " + str(len(coll_bits))
#    print coll_bits
    values = []
    # 需要使用int才能使用位操作
    int_count = int(math.ceil(len(coll_bits) / 32.0)) #留出余量
    for i in range(0, int_count):
        value = 0
        for j in range(0, 32):
            bit = 0
            index = i * 32 + j
            if (index < len(coll_bits)):
                bit = int(coll_bits[index])
            value = value << 1
            value = value | bit

        values.append(value)

    return values

def write_collect_bits(output_file, image, size = 4):

    values = get_collect_bits(image, size, 1)

    # 写入扫描的间隔
    output_file.WriteInt(size)
    
    # 输出byte位长度
    output_file.WriteInt(len(values) * 4)
    
    for v in values:
        # 使用big_endian保证Int内四个byte的顺序
        data = struct.pack('>I', v)
        output_file.Write(data)
  
def export_collect_bits(image_path):
    out_path = os.path.join(os.path.dirname(image_path), "data")
    out_file = FileWriter(out_path)

    image = Image.open(image_path)
    
    # 对每个像素输出扫描信息
    size = 1
    values = get_collect_bits(image, size)
    
    # 写入图片的长宽
    out_file.WriteInt(image.size[0])
    out_file.WriteInt(image.size[1])
    
    # 写入扫描的间隔
    out_file.WriteInt(size)
    
    # 输出byte位长度
    out_file.WriteInt(len(values) * 4)
    
    # 写数据体
    for v in values:
        # 使用big_endian保证Int内四个byte的顺序
        data = struct.pack('>I', v)
        out_file.Write(data)
    
def main(argv):
    parser = argparse.ArgumentParser(description="scan pictures, get bit information")
    parser.add_argument('-i', '--input', help='input image', dest="input", default=".")
    
    args = parser.parse_args()

    image_path = args.input
    
    export_collect_bits(image_path)

if __name__ == "__main__":
    main(sys.argv[1:])
