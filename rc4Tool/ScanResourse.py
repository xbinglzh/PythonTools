#!/usr/bin/python2.7.5
#conding=utf-8

import re
import os
import shutil
from Rc4Plist import Rc4Plist
from Rc4Png import Rc4Png

class ScanResourse:
    
    def __init__(self):
        self.__rc4PlistUtil = Rc4Plist()
        self.__rc4PngUtil = Rc4Png()
        self.__rootBase = "/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/9/"
        self.__plainDir = "Resources/"
        self.__encryptDir = "Resources_rc4/"
	
        self.__KPLIST = "plist"
        self.__KPNG = "png"
        self.__KTMX = "tmx"
        self.__KFNT = "fnt"
        self.__KCCB = "ccb"
        self.__KCCBPROJ="ccbproj"
	
        self.__RC4ROOT__ = [
            self.__rootBase + self.__encryptDir + "anim",
            self.__rootBase + self.__encryptDir + "battle",
            self.__rootBase + self.__encryptDir + "icons",
            self.__rootBase + self.__encryptDir + "ui",
            self.__rootBase + self.__encryptDir + "x_plist",
            self.__rootBase + self.__encryptDir + "xx_anim",
            self.__rootBase + self.__encryptDir + "xx_battle_map",
            self.__rootBase + self.__encryptDir + "xx_battle_ui",
            self.__rootBase + self.__encryptDir + "xx_card",
            self.__rootBase + self.__encryptDir + "xx_role_img",
            self.__rootBase + self.__encryptDir + "xx_ui",

            self.__rootBase + self.__encryptDir + "font/resources-ipad",
            self.__rootBase + self.__encryptDir + "font/resources-ipadhd"
	                                    
        ]
        
    def __copyResourse__(self,oldResPath,newResPath):
        shutil.copytree(oldResPath,newResPath)
    
    
    def main(self):
       
        inRes = self.__rootBase + self.__plainDir
        outRes =self.__rootBase + self.__encryptDir

        reNameInRes = self.__rootBase + "Resources_unRc4"
        reNameOutRes = self.__rootBase + "Resources"
	
        print "copy Resourse"
        self.__copyResourse__(inRes,outRes)
        print "rc4 File"
	
        for needRc4Dir in self.__RC4ROOT__:
            self.__traversalDirRc4__(needRc4Dir)

        print "rename Resourse"

        os.rename(inRes, reNameInRes)
        os.rename(outRes, reNameOutRes)

        print "Rc4 Over"
        
	
    #----------------------------------------------------------------------
    def __traversalDirRc4__(self , path):
	
        if not os.path.isdir(path) and not os.path.isfile(path) :
            return False

        if os.path.isfile(path):
            file_path = os.path.split(path)
            fileNameList = file_path[1].split('.')
            file_ext = fileNameList[-1]
		    
            if file_ext == self.__KPLIST:
                self.__rc4PlistUtil.readPlist2Rc4(path,path)
            elif file_ext == self.__KPNG:
                self.__rc4PngUtil.readPng2Rc4(path,path)
            elif file_ext == self.__KCCB:
                if os.path.exists(path) :
                    shutil.rmtree(file_path[0])
            elif file_ext == self.__KCCBPROJ:
                os.remove(path)
		    
        elif os.path.isdir(path):
            for x in os.listdir(path):
                self.__traversalDirRc4__(os.path.join(path,x))
	

if __name__ == "__main__": 
    scanRes = ScanResourse()
    scanRes.main()
