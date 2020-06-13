import os
import subprocess
import sys
import wget
import os
import requests
from time import time
from multiprocessing.pool import ThreadPool
import shutil
from colorama import Fore, Back, Style
import fileinput
from pathlib import *
import pathlib
from sys import platform


def dependency_check():
    a=['apktool.jar', 'd2j-dex2jar.bat', 'jd-gui-1.5.1.jar', 'signapk.jar']
    for x in a:
        if x in os.listdir():
            #print(x)
            print( "[+] "+x + "-> " +"check done")
        else:
            print("[-] "+x +" -> "+ "not check done")
            print("[-------]"+ x + "->"+"  please download and put in this folder")
            exit(0)


#--------------------------------------------------------------------------------------------------------------------------------------------------------


def app_decompile():

    cmd ="java -jar" +" "+"apktool.jar d"
    cmd1 = "java -jar" +" "+"apktool.jar b --use-aapt2"
    global file
    global file1
    file = input("enter path name of file")
    print("please wait your decompilation is in process")
    p = Path(file)
    print("[~~] input filename " +" "+str(p));
    a=p.name;
    #d=a+"1"+".apk"
    print(a);
    decompile=a.rsplit('.', 1)[0] ;
    c=decompile+"1.apk" ;
    print("[~~] Output filename " +" "+str(c));
    #print(c);
    #return_path =decompile+
    save_path = os.getcwd();
    b = "../"+decompile ;

    path2 =save_path+"/"+b ;
    status,result = subprocess.getstatusoutput(cmd +" "+file+" "+"-o"+path2+" "+"-f");
    print(result);
    return status,path2,p,decompile,cmd,cmd1,c,a;

#_________________________________________________________________________________________________________________________________________
def debug_check(path2):
     #status = ["True","False"]
     print("opening androidmainfest.xml file")
     f= open(path2+"/"+"AndroidManifest.xml","r");
     if 'android:debuggable="true"' in f.read():
          #print("debug is enabled");
          return True;
     else:
         print("app is not debuggable")
         return False;

#________________________________________________________________________________________________________________________________________
def extract_dex(p,decompile):
    print("extracting classes.dex file from  your build apk");
    extract_path ="../"+str(decompile)+"_"+"dex_files"
    print(extract_path)
    cmd3  =  "7za x"+" "+str(p)+" "+"-aoa"+" "+"classes*"+" "+"-o"+"."+"."+"/"+str(decompile)+"_"+"dex_files";
    #print(cmd3)
    #print(p,a)
    #print(str(p))
    status,result = subprocess.getstatusoutput(cmd3);
    print(status)
    #print(result)
    return status,extract_path

#___________________________________________________________________________________________________________________________________
def final_part(extract_path):
     cmd0= "java -jar"+" "+"baksmali.jar d"
     #dir_list = os.listdir(extract_path)
     #print([dir_list])

     #print(os.getcwd())

     for f in os.listdir(extract_path):
        print([f])
        final_path ="../final_output"
        status,result = subprocess.getstatusoutput(cmd0 +" "+extract_path+"/"+f+" "+"-o"+" "+final_path);
        print(status)
        return status,final_path

#_______________________________________________________________________________________________________________________________________

def recompile(path2,cmd1,p):
    print("[+]app recompile process started")
    with fileinput.FileInput(path2+"/"+"AndroidManifest.xml", inplace=True, ) as file:
            for line in file:
                print(line.replace('<application', '<application android:debuggable="true" '), end='')
                fileinput.close()
    
    status,result = subprocess.getstatusoutput(cmd1 +" "+path2);
    print(result);
    return status;

#____________________________________________________________________________________________________________________________________

def apk_signer(path2,a,p,c):
    print("application signing process started please wait");
    final_path=path2+"/"+"dist"+"/"+str(a);
    int_path = path2+"/"+"dist";

    #final_path =final_path+".apk"
    print(final_path)
    print("[+]sigining process started")
    cmd5 =  "java -jar signapk.jar certificate.pem key.pk8" +" "+final_path+" "+int_path+"/"+c;
    status,result = subprocess.getstatusoutput(cmd5);
    #print(result);
    return status,int_path;
#_________________________________________________________________________________________________________________________________

def main():
    os.chdir(os.getcwd()+"/"+"TOOLS")
    dependency_check()
    print("[+] application decompilation process started")
    #x= app_decompile()
    status,path2,p,decompile,cmd,cmd1,c,a = app_decompile()
    #print(path2)
    #print(status)
    if status==0:
        print("app is decompile completely")
        print("[++] checking app is debuggable or not")
        result =debug_check(path2)
        if(result==True):
            print("good , it takes some less time")
            status,extract_path=extract_dex(a,p)
            if status==0:
                print("[+]  all dex files are extracted completely[+]")
                final_part(extract_path)
                #print("[+][+] SIMPLE INSTALL THE DEBUGGABLE APPLICATION IN YOUR PHONE AND"+" [+]"+ final_path+" import this directory in your android studio" )


        else:
            print("give me some time we have to  recompile the application")
            status =recompile(path2,cmd1,p)
            if(status==0):
                print("[+] app recompile process completed")
                print("[+]{+}app signing proccess to start")
                status,int_path=apk_signer(path2,a,p,c)
                if status==0:
                    print("signapk sucess")
                    status,extract_path=extract_dex(p,decompile)
                    print(status);
                    if status==0:
                        print("[+]  all dex files are extracted completely[+]")
                        status,final_path=final_part(extract_path)
                        if status ==0:
                            print("[+][+] SIMPLE INSTALL THE DEBUGGABLE APPLICATION IN YOUR PHONE AND"+" [+]"+ final_path+" import this directory in your android studio" )
                        else:
                            Print("some error occured");

    else:

        print(path2)
        print("[-] some error comes sorry we are exiting");
        exit(0)






if __name__ == '__main__':
    main()
