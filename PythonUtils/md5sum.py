from functools import partial
import argparse
import hashlib
import sys

def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
            
    return d.hexdigest()

def main(argv):
    parser = argparse.ArgumentParser(description="get md5 sum information")
    parser.add_argument('-i', '--input', help='input image file', dest="input", default=".")
    
    args = parser.parse_args()

    image_path = args.input
    
    md5 = md5sum(image_path)

    print(md5)

if __name__ == "__main__":
    main(sys.argv[1:])
