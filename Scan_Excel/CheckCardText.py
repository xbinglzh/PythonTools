#!/usr/bin/python2.7.5
#coding:utf-8


import os
import sys
import getopt
from biplist import *

class CheckCard :

    def __readPlistByPath__(self,pPath):
        global plist_dict
        plist_dict={}
        plist_dict = readPlist(pPath)

        # print plist_dict

        return plist_dict

    def __checkError__(self):

        for key,value in dict(plist_dict).items():

            keyDisplay = ''
            cDisplay = ''

            for key2, value2 in dict(value).items():

                if key2 == 'type' :
                    keyDisplay =  value2 + '#display'

                if key2 == 'display':
                    cDisplay = value2

            if  keyDisplay != cDisplay :

                print  'error : ' + key + '  type : ' + keyDisplay + '  display : ' + cDisplay

        pass

    def main(self):
        global in_path
        global prefix_num
        global out_path

        self.__readPlistByPath__('/Users/user/Documents/Develop/PythonTools/Python_sacn_Tool/1/x_card.plist')
        self.__checkError__()

if __name__ == "__main__":
    checkCard = CheckCard()
    checkCard.main()
