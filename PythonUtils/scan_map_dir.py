#coding: utf-8

'''
Created on 2012-11-23

'''
import argparse
import map_scan
import os
import sys

'''
    扫描目录，找到所有map文件，并处理之
'''

def scanDir(directory):
    global filenum
            
    file_list = os.listdir(directory)
    for line in file_list:
        if line.startswith("."):
            print line
            continue 

        file_path = os.path.join(directory, line)
        
        if os.path.isdir(file_path):
            scanDir(file_path)
            pass
        else:
            ext = os.path.splitext(file_path)[-1]
            
            if ext == ".map":
                map_scan.scan_map(file_path, res_dir)
                
        filenum += 1

filenum = 0
res_dir = None

def main(argv):
    global res_dir
    
    parser = argparse.ArgumentParser(description="scan assert directory, get and parse .map")
    parser.add_argument('-i', '--input', help='input assest dir', dest="input", default=".")
    parser.add_argument('-r', '--resource', help='resource dir', dest="res", default=None)
    
    args = parser.parse_args()

    assets_dir = args.input
    res_dir = args.res
    
    scanDir(assets_dir)

if __name__ == "__main__":
    main(sys.argv[1:])