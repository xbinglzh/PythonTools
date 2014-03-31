'''
Created on Apr 26, 2011

'''
import struct
import array
import os

class FileWriter():
    '''
    classdocs
    '''
    def WriteFileHead(self):
        # write byte order, but the Value of Java Big/Lit end order?
        self.WriteByte(4)
        # num of Modle
        self.WriteBigInt(1)
        # write i
        self.WriteBigInt(1)
    
    def __Write(self, data):
        self.file.write(data)
        
    def WriteAny(self, i, typedef='f'):
        data = struct.pack(typedef, i)
        self.__Write(data)
    
    def WriteByte(self, b):
        data = struct.pack('B', b)
        self.__Write(data)
        
    def WriteBigInt(self, i):
        data = struct.pack('>i', i)
        self.__Write(data)
        
    def WriteInt(self, i):
        data = struct.pack('i', i)
        self.__Write(data)
        
    def WriteShort(self, i):
        data = struct.pack('h', i)
        self.__Write(data)
        
    def WriteFloat(self, f):
        data = struct.pack('f', f)
        self.__Write(data)
        
    def WriteLong(self, l):
        data = struct.pack('l', l)
        self.__Write(data)
        
    def WriteArray(self, array, typedef='f'):
        for i in array:
            self.WriteAny(i, typedef)

    def WriteArrayList(self, list, typedef='f'):
        for array in list:
            self.WriteBigInt(len(array))
            self.WriteArray(array)
        self.WriteBigInt(-1)
            
    def WriteList(self, l, typedef='h'):
        for i in l:
            self.WriteAny(i, typedef)
    
    
    def WriteString(self, us):
        # from unicode to string
        s = us.encode('ascii', 'ignore')
        self.WriteAny(len(s), 'i')
        data = struct.pack("%ds" % len(s), s)
        self.__Write(data)
        
    def Write3DVector(self, pValue):
        self.WriteFloat(pValue[0])
        self.WriteFloat(pValue[1])
        self.WriteFloat(pValue[2])
        
    def Write(self, data):
        self.__Write(data)
        
    def close(self):
        self.file.close()

    def __init__(self, fileName):
        '''
        Constructor
        '''
        
        out_dir = os.path.dirname(fileName)
        if not (os.path.exists(out_dir) & os.path.isdir(out_dir)):
            try:
                os.makedirs(out_dir)
            except:
                pass
        
        self.file = open(fileName, 'wb')