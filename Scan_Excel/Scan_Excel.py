#!/usr/bin/python2.7.5
#coding:utf-8

import argparse
import os
import sys
import getopt
from biplist import*
from pyExcelerator import*

class  ScanExcel:
    
    def __genKeyDict__(self,xlsPath):  
        global  _excel_list
        global _excel_dict
        global _keyDict
            
        _excel_list = parse_xls(xlsPath)
        _excel_dict = _excel_list[0][1]
        _keyDict={}
        for key,value in dict(_excel_dict).items():
            if isinstance(key,tuple) :
                if key[0]==0:
                    _keyDict[key[1]] = _excel_dict.get(key)        
       
                    
    def __excelDict2PlistDict__(self,inXlsPath):
        self.__genKeyDict__(inXlsPath)
        
        global _plist_dict
        _plist_dict ={}
        
        global map_data
        map_data = {}    
        
        if 'id' in dict(_keyDict).values():

            for key,value in dict(_excel_dict).items():

                if isinstance(value,float):
                    value = self.__formatFloatToInt__(value)
                    value = self.__formatStr__(value)
                else:
                    value = self.__formatStr__(value)

                if isinstance(key,tuple):
                        
                    x = str(key[0])
                    y = str(key[1])
                        
                    if  map_data.has_key(x):
                            
                        if y == '0':
                            idValue = value
                            if idValue == 'id':
                                continue
                            if isinstance(idValue,float):
                                idValue = self.__formatFloatToInt__(idValue)
                            
                            _plist_dict[str(idValue)] = map_data.get(x)

                    else:
                        id_key_dict = {}
                        map_data[x] = id_key_dict

                        if y == '0':
                            idValue2 = value
                            if idValue2 == 'id':
                                continue
                            if isinstance(idValue2,float):
                                idValue2 = self.__formatFloatToInt__(idValue2)
                                    
                            _plist_dict[str(idValue2)] = map_data.get(x)
                                
                    if isinstance(value, unicode) and "@" in value:
                        var_value = str(value).split("@")
                            
                        if var_value[0] == "list":
                            map_data.get(x)[_keyDict.get(key[1])] = self.__strTransformList__( var_value[1])
                        elif var_value[0] =="dict":
                            map_data.get(x)[_keyDict.get(key[1])] = eval(var_value[1])
                    else:
                        if isinstance(value,float):
                            _excel_dict[key] = self.__formatFloatToInt__(value)
                                
                        map_data.get(x)[_keyDict.get(key[1])] = value
            
        else:
            for key,value in dict(_excel_dict).items():
                value = self.__formatStr__(value)
                if isinstance(key,tuple): 
                    if key[1] == 0:
                        _plist_dict[value] = dict(_excel_dict).get((key[0],key[1]+1))
                    else:
                        continue;
            
        return _plist_dict        

#----------------------------------------------------------------------
    def __strTransformList__(self,strValue):
        strList = []
        
        if '},' in str(strValue):
            for  strItem  in str(strValue).split('},'):
                if "}" not in strItem:
                    strItem = strItem +"}"
                    
                dictStr =str(strItem)[str(strItem).find('{'):str(strItem).find('}')+1]
                strList.append( eval(str(dictStr)))
                
        else:
            
            dictStr = strValue[ str(strValue).find('[') +1 : str(strValue).find(']')  ]
            strList.append(eval(str(dictStr)))
                 
        return strList           
    
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
            
                # save_plist_name = file_path.split('/')[2].split('.')[0]+".plist"
                #plist_path = out_path +save_plist_name
                    
                    tmpArray = file_path.split('/')
                    save_plist_name = tmpArray[len(tmpArray)-1].split('.')[0]+".plist"
                    plist_path = out_path + save_plist_name

                    try: 
                        print "prease-->" + file_path
                        writePlist(self.__excelDict2PlistDict__(file_path), plist_path,False)
                        filenum += 1
                    except (InvalidPlistException, NotBinaryPlistException), e:  
                        print "Press Excel To Plist bad happened:", e 
                        
    def sacnExcelDir(self,intputDir,outPutDir):
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
        
            #----------------------------------------------------------------------
    def __formatFloatToInt__(self, f_val):
        i_val = 0
        
        if int (f_val) == 0:
            if f_val == 0:
                i_val = int (f_val)
            else:
                i_val = f_val
        else:
            if  f_val / int (f_val)  == 1:
                i_val = int (f_val)
            else:
                i_val =  f_val
                
        return i_val
        #----------------------------------------------------------------------
    def __formatStr__(self , strValue):

        if  isinstance(strValue , unicode) :
            strValue.replace('\r','')

        return str(strValue)

    def main(self,argv):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
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
                
            #---------------------
            # try:
            #     #plistDictResult =
            #     writePlist(self.__excelDict2PlistDict__('./1/x_reward.xls'), './2/x_reward.plist', False)
            #
            # except (InvalidPlistException, NotBinaryPlistException), e:
            #     print "Something bad happened:", e




if __name__ == "__main__": 
    
    scanExcel = ScanExcel()
    scanExcel.main(sys.argv[1:])
    


