#!/usr/bin/python3
'''
Created on 10.09.2012

@author: actionluzifer
'''

import subprocess
import sys
import os
import re

class MediaInfo(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        DARre = "(.*)DAR (?P<DAR>(.)*)](.*)"
        self.DAR_REprogramm = re.compile(DARre)
        PARre = "(.*)PAR (?P<PAR>(.)*) DAR(.*)"
        self.PAR_REprogramm = re.compile(PARre)
        
        
    def getInfo(self, _filename):
        print(" -> ",_filename)
        proc = subprocess.Popen(['avconv', "-i", _filename], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE);
        proc.stdin.close();
        proc.wait();
        
        sstr = ""
        for istring in proc.stdout:
            sstr = sstr+istring.decode() 
        
        return sstr
        

    def check4Paths(self, moveListen):
        print()
        print("Ordner anlegen: ...")
        for darname, darlist in moveListen.items():
            print("DAR Liste: "+darname)
            for parname, parlist in darlist.items():
                print("    PAR Liste: "+parname)
                path = darname+"/"+parname
                if os.path.exists(os.path.normpath(path)):
                    print(path," existiert")
                else:
                    print("    --> angelegt: ",path)
                    os.makedirs(path)
        print("...done")


    def getDPInfo(self, _infostr):
        resultDAR = None
        resultPAR = None
        foundDAR = self.DAR_REprogramm.search(_infostr)
        foundPAR = self.PAR_REprogramm.search(_infostr)
        if foundDAR:
            resultDAR = foundDAR.group("DAR").replace(":","_")
        if foundPAR:
            resultPAR = foundPAR.group("PAR").replace(":","_")
        return resultDAR, resultPAR


def moveMovie(movie, dar, par):
    head, tail = os.path.split(movie) 
        
    ## Schauen ob HEAD existiert
    if head == "":
        newpath = dar+"/"+par+"/"+tail
    else:
        newpath = head+"/"+dar+"/"+par+"/"+tail
    newpath = os.path.normpath(newpath)

    ## Pfad existiert, jetzt kann verschoben/umbenannt werden
    try:
        print("rename ",movie ," to: ",newpath)
        os.rename(movie, newpath)
        
        htm_old = movie.replace("avi","htm")
        htm_new = newpath.replace("avi","htm")
        print("rename ",htm_old ," to: ",htm_new)
        try:
            os.rename(htm_old, htm_new)
        except:
            return
    except:
        print("ups!!!!!!")
        
if __name__ == '__main__':
    moveListen = {}
    mediaInfo = MediaInfo()
    print("Bearbeite: ")
    for arg in sys.argv[1:]:
        info = mediaInfo.getInfo(arg)
        dar, par = mediaInfo.getDPInfo(info)
        if dar is not None:
            darlist = moveListen.get(dar, None)
            if  darlist is None:
                darlist = {}
                moveListen[dar]=darlist
                darlist['empty'] = []

            if par is not None:
                parlist = darlist.get(par, None)
                if parlist is None:
                    parlist = []
                    darlist[par]=parlist
            else:
                parlist = darlist.get('empty')
                
            parlist.append(arg)

    mediaInfo.check4Paths(moveListen)

    print("\n")
    for darname, darlist in moveListen.items():
        print("DAR Liste: "+darname)
        for parname, parlist in darlist.items():
            print("    PAR Liste: "+parname)
            for moviename in parlist:
                print("        "+moviename)
                moveMovie(movie=moviename, dar=darname, par=parname)
