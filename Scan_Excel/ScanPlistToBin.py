#!/usr/bin/python2.7.5
#conding=utf-8

import argparse
import os
import sys
import getopt
import struct
from biplist import *

########################################################################
class ScanPlistToBin:

    def __init__(self):
        pass
        
    def __readPlistByPath__(self,pPath):
        global plist_dict ;
        plist_dict={}
        plist_dict = readPlist(pPath)
        return plist_dict    
    
    #----------------------------------------------------------------------
    def __genBin__(self,outPut):
        writePlist(plist_dict, outPut, True)
        
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
                if ext == ".plist":
                    tmpArray = file_path.split('/')
                    save_plist_name = tmpArray[len(tmpArray)-1].split('.')[0]+".plist"
                    plist_path = out_path + save_plist_name
                                    
                    try: 
                        #print "prease-->" + file_path
                        self.__readPlistByPath__(file_path)
                        self.__genBin__(plist_path);
                        filenum += 1
                    except (Exception), e:  
                        print " Plist To Excel bad happened:", e        
                        
    def  sacnPlist2Bin(self,intputDir,outPutDir):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )    
        global in_path
        global prefix_num
        global out_path
                                
        in_path =  intputDir
        prefix_num = len(in_path)
        out_path = outPutDir
                                
        if in_path!="." and out_path!="xx.plist": 
            self.__scanDir__(in_path)
                                    
        return "Success change Excel Num: "+ str(filenum)                 
    
    def main(self,argv):
        global in_path
        global prefix_num
        global out_path
                 
        reload(sys)
        sys.setdefaultencoding( "utf-8" )          
                 
        parser = argparse.ArgumentParser(description="scan root excel")
        parser.add_argument('-i','--input',help='input excel file',dest = "input",default = ".")
        parser.add_argument('-o', '--output', help='out file', dest="output", default="xx.plist")    
        args = parser.parse_args()
                 
        in_path = args.input
        prefix_num = len(in_path)
        out_path = args.output
                 
        if in_path!="." and out_path!="xx.plist": 
            self.__scanDir__(in_path)
            print "Success change Num: "+ str(filenum)
        else:
            print "Please input args or look help(-h)"    

        #self.__readPlistByPath__('./Dir_Excel_2_Plist/x_card.plist')
        #self.__genBin__('./Dir_Plist_2_Excel/x_card.plist')
             
if __name__ == "__main__": 
    sacnPlistToBin = ScanPlistToBin()
    sacnPlistToBin.main(sys.argv[1:])        
        
        
    
    



