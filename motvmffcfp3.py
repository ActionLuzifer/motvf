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
        print("result: ",result,"")
        
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
        foundObject = REprogramm.search(_infostr)
        if foundObject:
            return foundObject.group("DAR")
        return None
        
        
def moveMovie(movie, dar):
    dar = dar.replace(":","_")
    head, tail = os.path.split(movie) 
    if (head != "" and os.path.exists(head+"/"+dar)) or (head == "" and os.path.exists(dar)):
        if head == "":
            newpath = dar+"/"+tail
        else:
            newpath = head+"/"+dar+"/"+tail
        if not os.path.exists(newpath):
            try:
                print("rename ",movie ," to: ",newpath)
                os.rename(movie, newpath)
                
                htm_old = movie.replace("avi","htm")
                htm_new = newpath.replace("avi","htm")
                print("rename ",htm_old ," to: ",htm_new)
                os.rename(htm_old, htm_new)
            except:
                print("ups!!!!!!")
        
if __name__ == '__main__':
    mediaInfo = MediaInfo()
    mediaInfo.check4Paths()
    print(sys.argv[1])
    for arg in sys.argv:
        info = mediaInfo.getInfo(arg)
        dar = mediaInfo.getDAR(info)
        if dar is not None:
            moveMovie(movie=arg, dar=dar)
    print("\n")
