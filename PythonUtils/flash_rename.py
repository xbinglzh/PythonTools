'''
Created on 2012-10-30
'''
import argparse
import sys
import os
import glob

class FlashRename:
    def __init__(self):
        self.showman_map = {
                     "00":"wing/L",
                     "01":"weapon/",
                     "02":"wing/R",
                     "03":"leg/L_L",
                     "04":"leg/L_R",
                     "05":"arm/A_L",
                     "06":"body/B",
                     "07":"head/H_NU",
                     "08":"glasses/",
                     "09":"arm/A_R",
                     "10":"head/H_XIAO",
                     "11":"head/H",
                     "12":"head/H_ZHAYAN",
                     }
        
        self.man_map = {
                     "00":"wing/L",
                     "01":"weapon/",
                     "02":"wing/R",
                     "03":"leg/L_L",
                     "04":"leg/L_R",
                     "05":"arm/A_L",
                     "06":"body/B",
                     "07":"head/H_XIAO",
                     "08":"glasses/",
                     "09":"arm/A_R",
                     "10":"head/H_NU",
                     "11":"death/11",
                     "12":"death/12",
                     "13":"death/13",
                     "14":"head/H",
                     "15":"under/15",
                     "16":"under/16",
                     "17":"under/17",
                     "18":"head/H_ZHAYAN",
                        }
        
        self.map = self.showman_map
        
    def replace_xml(self, xml_file, replace_map):
        f = open(xml_file, "r")
        
        s = f.read()
        
        for key in replace_map.keys():
            s = s.replace(key+".png", replace_map[key])
            
        f = open(xml_file, "w")
        f.write(s)
        
def main(argv):
    parser = argparse.ArgumentParser(description="rename flash xml")
    parser.add_argument('-i', '--input', help='input xml dir', dest="input", default=".")
    
    args = parser.parse_args()

    xml_dir = args.input
    
    list_path = os.path.join(xml_dir, "*.xml")
    xml_paths = glob.glob(list_path)
    
    rename_util = FlashRename();
    
    for xml in xml_paths:
        rename_util.replace_xml(xml, rename_util.man_map)

if __name__ == "__main__":
    main(sys.argv[1:])
        