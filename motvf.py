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
        if os.name == 'nt':
            head, tail = os.path.split(sys.argv[0]) 
            program = os.path.normpath(head+'\\libav-win32-pthreads-20130324\\usr\\bin\\avconv.exe')
            print(program)
        else:
            program = 'avconv'
        print(" -> ",_filename)
        proc = subprocess.Popen([program, "-i", _filename], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE);
        proc.stdin.close();
        proc.wait();
        
        sstr = ""
        for istring in proc.stdout:
            try:
                sstr = sstr+istring.decode()
            except:
                sstr = sstr+istring.decode('ISO-8859-1') 
        
        return sstr


    def getDPInfo(self, _infostr):
        resultDAR = None
        resultPAR = None
        foundDAR = self.DAR_REprogramm.search(_infostr)
        foundPAR = self.PAR_REprogramm.search(_infostr)
        if foundDAR:
            resultDAR = foundDAR.group("DAR").replace(":","_")
        else:
            resultDAR = None
        if foundPAR:
            resultPAR = foundPAR.group("PAR").replace(":","_")
        else:
            resultPAR = None
        return resultDAR, resultPAR


def moveMovie(movie, dar, par):
    head, tail = os.path.split(movie) 
        
    ## Schauen ob HEAD existiert
    if head == "":
        if "16_9" in dar:
            if ("64_45" in par) or ("1_1" in par):
                newpath = dar+"/"+tail
            else:
                newpath = dar+"/"+par+"/"+tail
        elif "4_3" in dar:
            if ("16_15" in par) or ("1_1" in par):
                newpath = dar+"/"+tail
            else:
                newpath = dar+"/"+par+"/"+tail 
        else:
            newpath = dar+"/"+par+"/"+tail
    else:
        if "16_9" in dar:
            if ("64_45" in par) or ("1_1" in par):
                newpath = head+"/"+dar+"/"+tail
            else:
                newpath = head+"/"+dar+"/"+par+"/"+tail
        elif "4_3" in dar:
            if ("16_15" in par) or ("1_1" in par):
                newpath = head+"/"+dar+"/"+tail
            else:
                newpath = head+"/"+dar+"/"+par+"/"+tail 
        else:
            newpath = head+"/"+dar+"/"+par+"/"+tail
    newpath = os.path.normpath(newpath)

    ## Pfad erstellen
    if not os.path.exists(os.path.split(newpath)[0]):
        os.makedirs(os.path.split(newpath)[0])

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


def searchFiles(args):
    newfiles = []
    for a in args:
        print(a)
    for arg in args:
        if ('--dry-run' == arg) or ('-d' == arg):
            isDryRun = True
        else:
            isDryRun = False
            head, tail = os.path.split(arg)
            tail = tail.replace("*", ".*")
            if head == "":
                head
            files=os.listdir(head)
            for file in files:
                if re.match(tail, file):
                    newfiles.append(os.path.normpath(head+"\\"+file))
    return isDryRun, newfiles


if __name__ == '__main__':
    print(sys.argv)
    if os.name == 'nt':
        isDryRun, args = searchFiles(sys.argv[1:])
    else:
        isDryRun = ('--dry-run' in sys.argv[1:]) or ('-d' in sys.argv[1:])
        args = sys.argv[1:]
    moveListen = {}
    mediaInfo = MediaInfo()
    print("Bearbeite: ")
    for arg in args:
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

    if isDryRun:
        for darname, darlist in moveListen.items():
            for parname, parlist in darlist.items():
                print(darname.replace("_",":")+" & "+parname.replace("_",":"))
    else:
        for darname, darlist in moveListen.items():
            print("DAR Liste: "+darname)
            for parname, parlist in darlist.items():
                print("    PAR Liste: "+parname)
                for moviename in parlist:
                    print("        "+moviename)
                    moveMovie(movie=moviename, dar=darname, par=parname)
