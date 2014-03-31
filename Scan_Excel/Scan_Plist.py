#!/usr/bin/python2.7.5
#conding=utf-8

import argparse
import os
import sys
import getopt
from biplist import *
from pyExcelerator import *

class ScanPlist:
    
    def __readPlistByPath__(self,pPath):
        global plist_dict ;
        plist_dict={}
        plist_dict = readPlist(pPath)
        return plist_dict        

#----------------------------------------------------------------------
    def __plistToExcel__(self):
        global header_key
        header_key = []
        j = 1
        
        for dict_item in dict(plist_dict).items():
            if len(header_key) == 0:
                if isinstance(dict_item[1],list):
                    header_key = dict( dict_item[1][0]).keys()
                elif isinstance(dict_item[1],dict):
                    header_key = dict( dict_item[1]).keys()
                elif isinstance(dict_item[1],str)  or isinstance(dict_item[1],unicode):
                    header_key = dict(plist_dict).keys()
                        
                if 'id' not in header_key:
                    header_key.append('id')
                
                header_key.sort()
                header_key.remove('id')
                header_key.insert(0,'id')
                    
                if isinstance(dict_item[1],str)  or isinstance(dict_item[1],unicode):
                    header_key.remove('id')
                    
                self.__headKeyToExcel__()
                
            if isinstance(dict_item[1],list):
                itemIndex = 0
                for item in dict_item[1]:
                    if 'id' not in dict( dict_item[1][0]).keys():
                        item['id'] = dict_item[0]  
                        
                    self.__dictToExcel__(item,j+itemIndex) 
                    itemIndex+=1
                        
            elif isinstance(dict_item[1],dict):
                if 'id' not in dict( dict_item[1]).keys():
                    dict_item[1]['id'] = dict_item[0]
                self.__dictToExcel__(dict_item[1],j)  
                
            elif isinstance(dict_item[1],str) or isinstance(dict_item[1],unicode):
                if j==1:
                    plist_dict['id'] = j
                    self.__dictToExcel__(plist_dict,j)
                       
            j+=1        
    
    def __dictToExcel__(self,value_dict,j):
        if isinstance(value_dict,dict):
            i = 0
            
            if 'id' in header_key:
                for key in header_key:    
                    if value_dict.get(key) != None:       
                        if isinstance (value_dict.get(key),list) :
                            workSheetWriter.write( j, i, "list@"+str(value_dict.get(key)))
                        elif (isinstance(value_dict.get(key),dict)):
                            workSheetWriter.write( j, i, "dict@"+str(value_dict.get(key)))
                        else:
                            workSheetWriter.write( j, i, value_dict.get(key)) 
                    i+=1                     
            else:
                for key in header_key:    
                    if value_dict.get(key) != None:       
                        if isinstance (value_dict.get(key),list) :
                            workSheetWriter.write( i, j, "list@"+str(value_dict.get(key)))
                            #workSheetWriter.write(j,i,"list@".join(value_dict.get(key)))
                        elif (isinstance(value_dict.get(key),dict)):
                            workSheetWriter.write( i, j, "dict@"+str(value_dict.get(key)))
                        else:
                            workSheetWriter.write( i, j, value_dict.get(key)) 
                    i+=1                
            
                   
    
    def __headKeyToExcel__(self):
        i = 0
        
        if  'id' in header_key :
            for var in header_key :
                workSheetWriter.write(0,i,var) 
                i+=1             
        else:
            for var in header_key :
                workSheetWriter.write(i,0,var) 
                i+=1             
        
    def __scanDir__(self,directory):
        global filenum
        filenum = 0
        global workSheetWriter
        
        file_list = os.listdir(directory)
        for line in file_list:
            if line.startswith("."):
                continue 
            file_path = os.path.join(directory, line)
            
            if os.path.isdir(file_path):
                self.scanDir(file_path)
                pass
            
            else:
                ext = os.path.splitext(file_path)[-1]
                
                if ext == ".plist":
                    tmpArray = file_path.split('/')
                    save_plist_name = tmpArray[len(tmpArray)-1].split('.')[0]+".xls"
                    plist_path = out_path + save_plist_name
                    
                    try: 
                        workExcel = Workbook() 
                        workSheetWriter = workExcel.add_sheet('sheet1')                    
                        self.__readPlistByPath__(file_path)
                        self.__plistToExcel__()
                        workExcel.save(plist_path)                     
                        filenum += 1
                    except (Exception), e:  
                        print " Plist To Excel bad happened:", e 
                    
    def scanPlistDir(self,inPath,outPath):
        global in_path
        global prefix_num
        global out_path
        in_path = inPath
        prefix_num = len(in_path)
        out_path = outPath
                
        if in_path!="." and out_path!="xx.plist": 
            self.__scanDir__(in_path)
            return "Success change Num: "+ str(filenum)
        else:
            return "Please input path"         
        
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
            
        # global workSheetWriter
        # workExcel = Workbook()
        # workSheetWriter = workExcel.add_sheet('sheet1')
        
        # self.__readPlistByPath__('./1/x_card.plist')
        # self.__plistToExcel__()
        # workExcel.save('./2/x_card.xls')
    
if __name__ == "__main__": 
        #main(sys.argv[1:])
    scanPlist = ScanPlist()
    scanPlist.main(sys.argv[1:])


