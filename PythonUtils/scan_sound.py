#coding: utf-8

'''
Created on 2012-12-17

扫描目录，清理出所有的音频文件，并列表输出
'''
import argparse
import os
import sys

def scanDir(directory, only_plist = False):    
    global filenum
    global prefix_num
    global plistImages
    global effects
    
    file_list = os.listdir(directory)
    for line in file_list:
        file_path = os.path.join(directory, line)
        if line.startswith("."):
            print file_path
            if os.path.isdir(file_path):
                os.removedirs(file_path)
            else:
                os.remove(file_path)
        elif os.path.isdir(file_path):
            out.write("\n")
            scanDir(file_path, only_plist)
        else:
            ext = os.path.splitext(file_path)[-1]
            relate_path = file_path[prefix_num:].replace("\\", "/")
                            
            if only_plist:
                if ext == ".json" or ext == ".plist":
                    file_name = os.path.basename(file_path)
                    image_name = os.path.splitext(file_name)[0] + ".png"
                    image_path = os.path.join(directory, image_name)
                    
                    if os.path.exists(image_path):
                        plistImages[image_path] = 1
                        
                        out.write("\"" + relate_path  + "\"," + "\n")
                    else:
#                        print "image error", "can't get image for: " + file_path + " image: " + image_path
                        raise Exception("image error", "can't get image for: " + file_path + " image: " + image_path)
            else:
                if ext == ".ogg":
                    if plistImages.has_key(file_path):
                        pass
                    else:
                        basename = line.split(".")[0]
                        
                        effects.append(basename)
                        
                        out.write("public static final SoundType " + basename  + " = new SoundType(R.raw." + basename + ", true);" + "\n")
                
            filenum += 1

filenum = 0
assets_dir = "."
prefix_num = 0
plistImages = {}

effects = []

out = None
def main(argv):
    global assets_dir
    global prefix_num
    global out
    global effects
    
    parser = argparse.ArgumentParser(description="scan assert directory, get texture information")
    parser.add_argument('-i', '--input', help='input assest dir', dest="input", default=".")
    parser.add_argument('-o', '--output', help='out file', dest="output", default="list.java")
    
    args = parser.parse_args()

    assets_dir = args.input
    prefix_num = len(assets_dir)
    out_file = args.output
    
    out = open(out_file, 'w')
    
    head = """  package com.droidhen.game.fa;

                import com.droidhen.game.ddt.R;
                import com.droidhen.game.sound.SoundType;

                // generate by scan_sound.py, don't edit this file by hand

                public class Sounds {"""
                        
    tail = """ }"""
    
    out.write(head)
    
    scanDir(assets_dir)
    
    out.write("public static final SoundType[] ALL_SOUNDS = {" + "\n")
    
    for effect in effects:
        out.write(effect + ",\n")
    
    out.write("};" + "\n")
    
    out.write(tail)


if __name__ == "__main__":
    main(sys.argv[1:])