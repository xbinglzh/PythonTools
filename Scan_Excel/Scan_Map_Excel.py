#!/usr/bin/python2.7.5
#coding:utf-8

import argparse
import os
import sys
import getopt
from biplist import *
from pyExcelerator import*

########################################################################
class ScanMapExcel :
        
    def __readExcel__(self,xlsPath):
        global _excel_list
        _excel_list = parse_xls(xlsPath)
                
    def __genPlistDict__(self,inPath):
        self.__readExcel__(inPath)
        global stage_dict
        stage_dict={}
                
        for stageKey,stageValue in dict(_excel_list).items() :
            postion_dict ={}

            for postionKey,postionValue in dict(stageValue).items():
                x = int(postionKey[1]) + 1
                y = int(postionKey[0]) + 1
                postionKey =(x,y)
                postion_dict[str(postionKey)] = postionValue
                stage_dict[str(stageKey)] = postion_dict
                
        return stage_dict
        
    def __scanDir__(self,directory):
        global filenum
        filenum = 0
        file_list = os.listdir(directory)
        for line in file_list:
            if line.startswith("."):
                continue
            file_path = os.path.join(directory, line)
                        
            if os.path.isdir(file_path):
                self.__scanDir__(file_path)
                pass
            else:
                ext = os.path.splitext(file_path)[-1]
                if ext == ".xls":
                    tmpArray = file_path.split('/')
                    save_plist_name = tmpArray[len(tmpArray)-1].split('.')[0]+".plist"
                    plist_path = out_path + save_plist_name
                                        
                    try:
                        print "prease-->" + file_path
                        writePlist(self.__genPlistDict__(file_path),plist_path,False)
                        filenum += 1
                    except (InvalidPlistException, NotBinaryPlistException), e:
                        print "Press Excel To Plist bad happened:", e
        

        def scanMap(self,inputRes,outputRes):
            global in_path
            global prefix_num
            global out_path
                
            in_path = inputRes
            prefix_num = len(in_path)
            out_path = outputRes
                                
            if in_path!="." and out_path!="xx.plist":
                self.__scanDir__(in_path);
                return "Success change Num: "+ str(filenum)
            else:
                return " input or output args is error"
                        
        def main(self,argv):
                
            global in_path
            global prefix_num
            global out_path
                  
            parser = argparse.ArgumentParser(description="scan root excel")
            parser.add_argument('-i','--input',help='input excel file',dest = "input",default = ".")
            parser.add_argument('-o', '--output', help='out plist file', dest="output", default=".")
                  
            args = parser.parse_args()
                  
            in_path = args.input
            prefix_num = len(in_path)
            out_path = args.output
                
            if in_path!="." and out_path!="xx.plist":
                self.__scanDir__(in_path);
                print "Success change Num: "+ str(filenum)
            else:
                print "Please input args or look help(-h)"

if __name__ == "__main__":
    #main(sys.argv[1:])
    scanMapExcel = ScanMapExcel()
    scanMapExcel.main(sys.argv[1:])

