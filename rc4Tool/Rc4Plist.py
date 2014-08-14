#!/usr/bin/python2.7.5
#conding=utf-8

import argparse
import os
import sys
import getopt
import struct
import commands
import SvnConfig
from biplist import *
from Rc4Util import RC4Util
########################################################################
class Rc4Plist:

    def __init__(self):
        self.rc4Util = RC4Util()
        
    def __readPlistByPath__(self,pPath):
        global plist_str
        global plist_dict
        plist_dict={}
        plist_dict = readPlist(pPath)

        plist_str = writePlistToString(plist_dict, True)

        # print str(plist_str).decode('utf-8').encode('utf-8')

        # unicode(plist_str, "utf-8")


        return plist_str
    
    def __genBin__(self,outPut):
        writePlist(plist_dict, outPut, False)
    
    def __Rc4__(self,outPut):
        encryptSrc = self.rc4Util.rc4(str(plist_str), "test")   
        b=open(outPut,'w+')
        b.write(encryptSrc)
        b.close()        
        
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
                    savePath = out_path + save_plist_name
                    
                    try: 
                        self.__readPlistByPath__(file_path)
                        self.__Rc4__(savePath)
                        filenum += 1
                    except (Exception), e:  
                        print " rc4 plist bin bad happended:", e        
                        
    def readPlist2Rc4(self,inPutFile,outPutFile):
        self.__readPlistByPath__(inPutFile)
        self.__Rc4__(outPutFile)
        
            
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
    
    def __svnCheckOut__(self):
        cmd = "svn up %(url)s %(dist)s" % SvnConfig.setting
        print "execute %s"%cmd
        return os.system(cmd)
    
    def __svnCheckIn__(self):
        cmd = "svn ci %(url)s %(dist)s" % SvnConfig.setting
        print "execute %s" % cmd
        return os.system(cmd)
        
    def main(self,argv):

        reload(sys)
        sys.setdefaultencoding( "utf-8" )

        global in_path
        global prefix_num
        global out_path
        
        in_path = "/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/6/"
        prefix_num = len(in_path)
        out_path = "/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/7/"

        
        self.__scanDir__(in_path)

if __name__ == "__main__": 
    sacnPlistToBin = Rc4Plist()
    sacnPlistToBin.main(sys.argv[1:])        
        
        
    
    



