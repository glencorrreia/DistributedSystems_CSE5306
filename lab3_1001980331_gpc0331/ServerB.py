#GLEN CORREIA
#1001980331
import datetime
import socket
import sys
import threading
from _thread import *
import os
from os import path
import re
import time
import os.path
from dirsync import sync
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def time_to_date(ts):
    a = datetime.datetime.fromtimestamp(ts)
    year = a.strftime("%Y")
    month = a.strftime("%m")
    day = a.strftime("%d")
    return month+"/"+day+"/"+year

src = "B_dir"
des = "A_dir"
#https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
#https://pythonhosted.org/watchdog/api.html
class Handler(FileSystemEventHandler):
    def create(event):
        sync(src, des, 'sync') #using sync func
        

    def delete(self, event):
        
        path = os.path.split(event.src_path)#split the list
        path = path[1]
        print(path)
        

        if os.path.exists("A_dir/"+path):
           os.remove("A_dir/"+path)
        else:
            pass

    # for modifying
    def modi(event):
        sync(src, des, 'sync')

class ClientThread(threading.Thread):
    def __init__(self, ClientAddr, ClientSock):
        threading.Thread.__init__(self)
        self.csocket = ClientSock
        print("New Client Connection Added from address: ", ClientAddr)

    def run(self):
        directory = 'B_dir'
        sync("B_dir","A_dir",'sync')
        

        while True:

            c = self.csocket.recv(2048) #blocking the connections
            c = c.decode()         #decode into format
            
            if c =="lab3":
                #see your own Directory
                SBList = os.listdir(directory)
                print(SBList)

                totalfiles = bytes(str(len(SBList)),'utf-8')
                self.csocket.sendall(totalfiles)

                SBfiles =[]
                for item in os.scandir(directory):
                    row = ( item.name , item.stat().st_size , time_to_date (item.stat().st_atime)   )
                    SBfiles.append(row)
                print("Files in Server B =>" ,SBfiles)
                print("Sending data to A......")

                
                for eachfile in SBfiles:
                    for filedata in eachfile:
                        filedata = str(filedata).encode()
                        print("send in loop:",filedata)
                        self.csocket.sendall(filedata)

                print("Send Data to A Complete !!!!")


            if c =="exit":
                print("ServerA Disconnected")
                                
            time.sleep(1)



if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 9091
#https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
    observer = Observer()#create observer
    event_handler = Handler() #create handler
    observer.schedule(event_handler,  "B_dir", recursive = False) #scheduling handler
    observer.start()
    
    #http://net-informations.com/python/net/thread.htm
    try:
        myserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        myserver.bind((HOST,PORT))
        print("Starting Server at HOST: "+ HOST + " and PORT: ", PORT)
        while True:
            myserver.listen(1)
            conn, addr = myserver.accept(    )#wait for new connection
            newclientthread = ClientThread(addr, conn)
            newclientthread.start()
    except Exception:
        print('Error occured')
    finally:
        myserver.close()




















