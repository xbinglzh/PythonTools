#!/usr/bin/python2.7.5
#conding=utf-8

import re
import os
import shutil
import sys,stat

class DeleteSvn :

    def __init__(self):

        pass

    def walk(self, path):

        __delCount = 0

        for item in os.listdir(path):
            subpath = os.path.join(path, item)
            mode = os.stat(subpath)[stat.ST_MODE]

            if stat.S_ISDIR(mode):
                if item == ".svn":
                    print "Cleaning %s ..." %subpath

                    var = self.purge(subpath)
                    __delCount += var

                else:
                    self.walk(subpath)

    def purge(self,path):
        count = 0
        for item in os.listdir(path):
            subpath = os.path.join(path, item)
            mode = os.stat(subpath)[stat.ST_MODE]

            if stat.S_ISDIR(mode):
                count = self.purge(subpath)
            else:
                os.chmod(subpath, stat.S_IREAD|stat.S_IWRITE)
                os.unlink(subpath)
                count = 1

        os.rmdir(path)
        count
        return count

    def main(self):

        self.walk("/Users/xUanBing/Documents/Developer/Github/HappyMouse/")
        pass

    pass

if __name__ == "__main__":
    deleteSvn = DeleteSvn()
    deleteSvn.main()