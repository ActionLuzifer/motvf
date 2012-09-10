#!/usr/bin/python3
'''
Created on 10.09.2012

@author: actionluzifer
'''

import subprocess
import sys
import os
import string
import re

class MediaInfo(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def getInfo(self, _filename):
        param = "-i "+_filename
        print("param: ",param)
        proc = subprocess.Popen(['avconv', "-i", _filename], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE);
        proc.stdin.close();
        proc.wait();
        
        result = proc.returncode;
        print("\nresult: ",result,"\n")
        
        sstr = ""
        for istring in proc.stdout:
            sstr = sstr+istring.decode() 
        
        return sstr
        

    def check4Paths(self):
        for path in ["16_9", "4_3"]:
            if os.path.exists(path):
                print(path," existiert")
            else:
                print("angelegt: ",path)
                os.mkdir(path)

    def getDAR(self, _infostr):
        DARre = "(.*)DAR (?P<DAR>(.)*)](.*)"
        REprogramm = re.compile(DARre)
        #for line in _infostr:
        foundObject = REprogramm.search(_infostr)
        if foundObject:
            #print(foundObject)
            print(foundObject.group("DAR"))
            return foundObject.group("DAR")
        return None
        
        
def moveMovie(movie, dar):
    dar = dar.replace(":","_")
    head, tail = os.path.split(movie) 
    print("head: ",head)
    print("tail: ",tail)
    if head == "":
        newpath = dar+"/"+tail
    else:
        newpath = head+"/"+dar+"/"+tail
    if not os.path.exists(newpath):
        print("rename to: ",newpath)
        os.rename(movie, dar+"/"+movie)
        htm = movie.replace("avi","htm")
        os.rename(htm, dar+"/"+htm)
        
if __name__ == '__main__':
    mediaInfo = MediaInfo()
    mediaInfo.check4Paths()
    print(sys.argv[1])
    for arg in sys.argv:
        info = mediaInfo.getInfo(arg)
        #print(info)
        dar = mediaInfo.getDAR(info)
        if dar is not None:
            moveMovie(movie=arg, dar=dar)
