#!/usr/bin/python2.7.5
#encoding=utf-8

import sys
import os,os.path
import zipfile
import argparse
import subprocess
import shutil
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement 

from ZipTool import ZFile

class ZipReName :  

    def __removeDir__(self, savePath):
        global filenum
        filenum = 0
                
        global removeFile
        removeFile = 0
                                        
        file_list = os.listdir(savePath)
        for line in file_list:
            if line.startswith("."):
                continue
            file_path = os.path.join(savePath, line)
                                        
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                filenum += 1

                pass
        
    def __scanDir__(self,directory):
            global filenum
            filenum = 0
                        
            file_list = os.listdir(directory)
            for line in file_list:
                if line.startswith("."):
                    continue
                file_path = os.path.join(directory, line)
                        
                if os.path.isdir(file_path):
                    #遍历子目录
                    self.__scanDir__(file_path)
                else:
                    ext = os.path.splitext(file_path)[-1]
                    if ext == ".zip":
                        tmpArray = file_path.split('/')
                                        
                        saveName = tmpArray[len(tmpArray)-1].split('.')[0] + ""
                                        
                        self.__doProcess__(file_path, out_path)
                                        
                        filenum += 1
                                        
                                        
    def __texturePack__(self, inputRes, outputRes, saveName):
                
            savePlistName = outputRes  + saveName +'.plist'
            savePngName   = outputRes  + saveName +'.png'
            scanPngRes    = inputRes
                
            cmd_1 = 'TexturePacker --format cocos2d --data  %(savePlistName)s ' % {'savePlistName' : savePlistName}
            cmd_2 = '--sheet %(savePngName)s --opt RGBA8888 --max-width 8192 --max-height 8192 ' % {'savePngName' : savePngName}
            cmd_3 = '--border-padding 0 --shape-padding 0 --size-constraints AnySize --premultiply-alpha '
            cmd_4 = scanPngRes+'*.png'
                             
            commandStr = cmd_1+cmd_2+cmd_3+cmd_4
                
            subprocess.Popen(commandStr, shell=True)
                
                
    def __modifyXML__(self,xmlFile, rename):
            tree = ElementTree.parse(xmlFile)
            root = tree.getroot()
                
            armature_Paramter = root.find("armatures").findall("armature")
                
            if armature_Paramter[0].attrib.has_key("name"):
                armature_Paramter[0].set("name", rename)
                                
                animation_Paramter = root.find("animations").findall("animation")  
                
                if animation_Paramter[0].attrib.has_key("name"):   
                    animation_Paramter[0].set("name", rename)
                                
                tree.write(xmlFile)  
                
                tmpArray = xmlFile.split('/')  
                
                shutil.move(xmlFile,tmpArray[0] +"/" + tmpArray[2])
                
    def __doProcess__(self, zip_path, savePath) :

        tmpArray = zip_path.split('/')
        fileName = tmpArray[len(tmpArray)-1].split('.')[0]

        # modifyZipArray = ['xx_m_206401d','xx_m_206201d','xx_m_200201d']
        #
        # if modifyZipArray.__sizeof__() > 0 :
        #     if fileName in  modifyZipArray :
        #         self.__runScript__( zip_path,savePath, fileName)
        # else:
        #     self.__runScript__( zip_path,savePath, fileName)

        self.__runScript__( zip_path,savePath, fileName)


    def __runScript__(self, zip_path, savePath, fileName):
        self.zipUtil = ZFile(zip_path)
        self.zipUtil.extractToRename(savePath + fileName)
        self.zipUtil.close()

        self.__modifyXML__(savePath + fileName + '/' + fileName +'.xml', fileName)
        self.__texturePack__(savePath + fileName + '/texture/', savePath, fileName)

                        
    def main(self,argv):
            reload(sys)
            sys.setdefaultencoding('utf-8')
                
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
                
            if in_path!="." and out_path!="xx.zip":

                self.__scanDir__(in_path)
                # self.__removeDir__(out_path)

                print "Success change Num: "+ str(filenum)
            else:
                print "Please input args or look help(-h)"
                        
                try:  
                ##self.zipUtil = ZFile('/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/zipRes/x_skill_912001.zip')
                    ##self.zipUtil.extractToRename('/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/zipOutRes')
                    ##self.zipUtil.close
                        
                    ##inRes = '/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/zipOutRes/texture/'
                    ##outRes = '/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/zipOutRes/'
                    ##saveName = 'textPlist'
                        
                    ##xmlRes = outRes + 'x_skill_912001_skeleton.xml'
                    ##self.__modifyXML__(xmlRes,x_skill_912001_skeleton)
                        
                    #self.__doProcess__('/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/5/xx_m_100001.zip', '/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/6/')
                    #out_path = '/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/6/'
                    #self.__scanDir__('/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/5')
                        
                    pass
                        
                except (Exception), e:  
                    print "Something bad happened:", e
                

if __name__ == "__main__": 
    zipRename = ZipReName()
    zipRename.main(sys.argv[1:])