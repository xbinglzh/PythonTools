# coding: utf-8
'''
Created on 2012-12-14

'''

import argparse
import re
import sys

class ErrorCode:
    def __init__(self, errorcode, errorcode_name, errorcode_text):
        self.code = errorcode
        self.name = errorcode_name
        self.text = errorcode_text
        
    def __str__(self):
        return "code: " + str(self.code) + " name: " + self.name + " text: " + self.text

class ErrorCodeScanner:
    def __init__(self, errorcode_file):
        self.errorcode_file = errorcode_file
        
        self.errorcodes = {}
        
        pass
    
    def read_errorcodes(self):
        in_codes = False
        
        f = open(self.errorcode_file)
        
        old_string = f.read()

        string = re.sub("\/\*(\s|.)*?\*\/", "", old_string)
        
        lines = string.splitlines()
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("//"):
                continue
            
            if (not in_codes) and (line.find("{") != -1):
                in_codes = True
                continue
                
            if in_codes and (line.find("}") != -1):
                in_codes = False
                continue
            
            if in_codes:
                splits = line.split(" ")
                
                if len(splits) <= 1:
                    continue
                
                print splits
                
                offset = 0
                if line.find("final") != -1:
                    offset = 1;
                
                errorcode_name = splits[3 + offset].lower()
                
                code_split = splits[5 + offset]
                index = code_split.find(";")
                if index != -1:
                    errorcode = code_split[:index]
                else:
                    errorcode = code_split
                    
                errorcode = int(errorcode)
                
                if line.find("//") != -1:
                    errorcode_text = line[line.find("//") + 2:]
                else:
                    errorcode_text = ""
                
                errCode = ErrorCode(errorcode, errorcode_name, errorcode_text)
                
                print errCode
                
                self.errorcodes[errorcode] = errCode
                
        ''' end '''
        print self.errorcodes
    
    def export_csv(self):
        with open(self.errorcode_file + ".csv", "w") as out:
            out.write("errorCode, name, text" + "\n")
            
            keys = self.errorcodes.keys()
            keys.sort()
            for code in keys:
                errorcode = self.errorcodes[code]
            
                out.write(str(errorcode.code) + ", " + errorcode.name + ", " + errorcode.text + "\n")
                
    
def main(argv):
    parser = argparse.ArgumentParser(description="Arrange map directory")
    parser.add_argument('-i', '--input', help='input errorcode file', dest="input", default=".")
    
    args = parser.parse_args()

    errorcode_file = args.input
    
    print "errorcode file: " + errorcode_file
    
    scaner = ErrorCodeScanner(errorcode_file)
    scaner.read_errorcodes()
    
    scaner.export_csv()
    
if __name__ == "__main__":
    main(sys.argv[1:])