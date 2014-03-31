#!/usr/bin/python2.7.5
#coding:utf-8

import zipfile   
import os.path   
import os   
   
class ZFile(object):   
    def __init__(self, filename, mode='r', basedir=''):   
        self.filename = filename   
        self.mode = mode   
        if self.mode in ('w', 'a'):   
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)   
        else:   
            self.zfile = zipfile.ZipFile(filename, self.mode)   
        self.basedir = basedir   
        if not self.basedir:   
            self.basedir = os.path.dirname(filename)   
          
    def addfile(self, path, arcname=None):   
        path = path.replace('//', '/')   
        if not arcname:   
            if path.startswith(self.basedir):   
                arcname = path[len(self.basedir):]   
            else:   
                arcname = ''   
        self.zfile.write(path, arcname)   
              
    def addfiles(self, paths):   
        for path in paths:   
            if isinstance(path, tuple):   
                self.addfile(*path)   
            else:   
                self.addfile(path)   
              
    def close(self):   
        self.zfile.close()   
          
    def extract_to(self, path):   
        for p in self.zfile.namelist():   
            self.extract(p, path)   
              
    def extract(self, filename, path):   
        if not filename.endswith('/'):   
            f = os.path.join(path, filename)  
            dir = os.path.dirname(f)   
            if not os.path.exists(dir):   
                os.makedirs(dir)   
            file(f, 'wb').write(self.zfile.read(filename))   
    
    
    def extractToRename(self, path):
        
        global saveName
        tmpArray = self.filename.split('/')
        saveName = tmpArray[len(tmpArray)-1].split('.')[0] + "" 
        
        for p in self.zfile.namelist():   
                    self.__extractReName__(p, path)        
            
    def __extractReName__(self, filename, path):
        self.extract(filename, path)
        self.__reNameSkeleton__(path, filename)
        
    def __reNameSkeleton__(self, path, name):
        
        if name == 'skeleton.xml' :
                oldName = path + "/" + name
                newName = path + "/" + saveName +'.xml'
                os.rename( oldName, newName)
        if name == '.DS_Store' :
                os.remove(path + "/" + name)        
              
          
#def create(zfile, files):   
    #z = ZFile(zfile, 'w')   
    #z.addfiles(files)   
    #z.close()   
      
#def extract(zfile, path):   
    #z = ZFile(zfile)   
    #z.extract_to(path)   
    #z.close()  