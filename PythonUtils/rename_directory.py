#encoding: utf-8

'''
Created on 2012-11-22

'''

import argparse
import os
import sys

'''
    扫描目录，清理出单张图片，plist等，以及动画的xml
'''

def scanDir(directory, target_depth = 0):
    """
        target_depth，指定给定目录下的几级目录发生rename事件
    """
    global filenum
    global path_depth
        
    curr_depth = path_depth[directory]
    
    print "dir: " + directory + " curr_depth: " + str(curr_depth) + " target target_depth: " + str(target_depth)
            
    file_list = os.listdir(directory)
    for line in file_list:
        if line.startswith("."):
            print line
            continue 

        file_path = os.path.join(directory, line)
        if os.path.isdir(file_path):
            path_depth[file_path] = curr_depth + 1
            
            scanDir(file_path, target_depth)
            pass
        else:
            if curr_depth != int(target_depth):
                continue
            
            ext = os.path.splitext(file_path)[-1]
            
            
            if ext == ".png" or ext == ".jpg":
                base_name = os.path.basename(file_path)
            
                dir_path = os.path.dirname(file_path)
                dir_name = os.path.basename(dir_path)
            
                dir_dir_name = os.path.dirname(dir_path)
                
                os.rename(file_path, os.path.join(dir_dir_name, dir_name + "_" + base_name))
                
        filenum += 1

filenum = 0
path_depth = {}
assets_dir = "."
def main(argv):
    global assets_dir
    global prefix_num
    
    parser = argparse.ArgumentParser(description="scan assert directory, get texture information")
    parser.add_argument('-i', '--input', help='input assest dir', dest="input", default=".")
    parser.add_argument('-d', '--depth', help='dir depth to be rename', dest="depth", default=0)
    
    args = parser.parse_args()

    assets_dir = args.input
    depth = args.depth
    
    path_depth[assets_dir] = 0
    scanDir(assets_dir, depth)

if __name__ == "__main__":
    main(sys.argv[1:])
