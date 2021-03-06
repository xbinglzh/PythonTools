#!/usr/bin/python2.7.5
#conding=utf-8

import os
import sys
import struct
from Rc4Util import RC4Util

########################################################################
class Rc4Png:
    
    def __init__(self):
        self.rc4Util = RC4Util()
    
    def main(self,argv):
        global in_path
        global out_path
            
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
        plainRoot = "/Users/pro/Documents/develop/dev_gexin/outsource/metalwar/MetalWarLostCity/Projects/iLostCity/iLostCity/png_bin/"

        in_path = plainRoot + "UIMainMapView.png"

        self.readPng2Rc4(in_path,in_path)
            
        #out_path = encryptRoot  + "achievement_badge.png"
            
        #plainImage = open(in_path,'r')
        #encryptImage = open(out_path,'w+')
            
        #encryptData = self.__encryptBinData__(plainImage.read())
        #encryptImage.write(encryptData)
            
        #plainImage.close()
        #encryptImage.close()
            
    #----------------------------------------------------------------------
    def readPng2Rc4(self,inPutFile,outPutFile):
        
        file_path = os.path.split(inPutFile)
        fileNameList = file_path[1].split('.')
        file_ext = fileNameList[-1]
	    
        save_path = inPutFile + "_"
	    
        plainImage = open(inPutFile,'r')
        encryptImage = open(save_path,'w+')
        encryptData = self.__encryptBinData__(plainImage.read())
        encryptImage.write(encryptData)
        plainImage.close()
        encryptImage.close()
	    
        os.remove(inPutFile)
        os.rename(save_path,inPutFile)
            
    #----------------------------------------------------------------------
    def __encryptBinData__(self, data):
        encryKey = 'test'
        data_top_r = self.rc4Util.rc4(data[0:33],encryKey) 
        new_data = data_top_r + data[33:]
        new_data_len = len(new_data)
        new_data_1 = new_data[0:new_data_len/2]
        new_data_2 = new_data[new_data_len/2:]
        new_data_top_r = self.rc4Util.rc4(new_data_2[0:10],encryKey)
        
        data = new_data_1 + new_data_top_r + new_data_2[10:]
        return data
        
    

if __name__ == "__main__": 
    rc4Png = Rc4Png()
    rc4Png.main(sys.argv[1:])
        
        
    
    