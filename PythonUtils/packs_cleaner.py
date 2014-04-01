# coding:utf-8

'''
Created on 2012-12-14

读取packer的json输出，并删除已经被拼接过的文件
'''

import argparse
import json
import sys
import os

def readJson(json_file, pic_dir):
    f = open(json_file, "r")
    
    string = f.read();
    
    pack = json.loads(string)
    
    pics = pack["frames"]
    
    print pics.keys()
    
    for pic in pics.keys():
        path = os.path.join(pic_dir, pic)
        
        os.remove(path)

def main(argv):
    parser = argparse.ArgumentParser(description="Arrange map directory")
    parser.add_argument('-i', '--input', help='input json file', dest="input", default=".")
    parser.add_argument('-d', '--dir', help='pics dir', dest="dir", default=".")
    
    args = parser.parse_args()

    json_file = args.input
    pics_dir = args.dir
    
    readJson(json_file, pics_dir)

if __name__ == "__main__":
    main(sys.argv[1:])