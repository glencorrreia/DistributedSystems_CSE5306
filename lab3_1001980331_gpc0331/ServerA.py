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
import os.path
import time
from dirsync import sync
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#create socket
def setup(HOST, PORT):
    #https://realpython.com/python-sockets/
    mc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mc.connect((HOST, PORT))
    return mc, HOST, PORT

def time_to_date(ts):
    z = datetime.datetime.fromtimestamp(ts) #to get the date
    year = z.strftime("%Y")
    month = z.strftime("%m")
    day = z.strftime("%d")
    return month+"/"+day+"/"+year

#---------------MAIN CODE---------------------------------#
src = "A_dir"
des = "B_dir"
Tl = []
#https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
#https://pythonhosted.org/watchdog/api.html
class Handler_A(FileSystemEventHandler):
    def create(self, event):

        sync(src,des,'sync',verbose = True, exclude = Tl )        
#https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder-in-python
    def delete(self, event):
        
        path = os.path.split(event.src_path)#split the list
        path = path[1]
        print(path)
        

        if os.path.exists("B_dir/"+path):
           os.remove("B_dir/"+path)
        else:
            pass
        

        
#for modifying 
    def modi(self,event): 
        sync(src, des, 'sync',verbose = True, exclude = Tl )
        

class Handler_B(FileSystemEventHandler):
    def create(self, event):

        sync(des,src,'sync',verbose = True, exclude = Tl )        
#https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder-in-python
    def delete(self, event):
        
        path = os.path.split(event.src_path)#split the list
        path = path[1]
        print(path)
        

        if os.path.exists("A_dir/"+path):
           os.remove("A_dir/"+path)
        else:
            pass
        

        
#for modifying 
    def modi(self,event): 
        sync(des, src, 'sync',verbose = True, exclude = Tl )
        


class ClientThread(threading.Thread):
    def __init__(self, ClientAddr, ClientSock):
        threading.Thread.__init__(self)
        self.csocket = ClientSock
        print("New Client Connection Added from address: ", ClientAddr)


    def run(self):
        
        directory = 'A_dir'
        sync("A_dir","B_dir",'sync',verbose = True, exclude = Tl)
        #Connect Server B
        HOST_B = '127.0.0.1'
        PORT_B = 9091
        serverA, HOST, PORT = setup(HOST_B, PORT_B)

        
        
                
         
        while True:

            print(Tl)
            c = self.csocket.recv(2048) 
            c = c.decode()
            c = c.split("-")
            print("Looking at A"+ str(c))
            if c[0].strip() == "lab3":
                #see your own Directory
                SAList = []
                for item in os.scandir(directory):
                    row = ( item.name , item.stat().st_size , time_to_date (item.stat().st_atime)   )
                    SAList.append(row)
                print("In my Server A =>" ,SAList)

                
                SAList.sort()
                
                print("before giving data:"+str(SAList))
                serverA.close()
                message = bytes(str(SAList),'utf-8')
                self.csocket.sendall(message)
            
            elif c[0].strip() == "lock":
                print("inside lock \n\n")
                listing = os.listdir(directory)
                print(listing)
                Tl.append(listing [int(c[1])])
            
            elif c[0].strip() == "unlock":
                print("inside unlock")
                listing = os.listdir(directory)
                print(listing)
                Tl.remove(listing [int(c[1])])
                sync("B_dir","A_dir",'sync',verbose = True,exclude = Tl)
                
            elif c[0] =="exit":
                print("Client Disconnected")
                                
                
            else:
                pass



if __name__ == "__main__":
   
    HOST = '127.0.0.1'
    PORT = 9090
    #https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
    observer = Observer() #create observer
    event_handler = Handler_A() #create handler
    observer.schedule(event_handler, "A_dir", recursive = False) #scheduling handler
    observer.start()

    event_handler_b = Handler_B()
    observer_B = Observer()
    observer_B.schedule(event_handler_b, "B_dir", recursive = False)
    observer_B.start()
            
    

    #http://net-informations.com/python/net/thread.htm
    try:
        myserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        myserver.bind((HOST,PORT))
        print("Starting Server at HOST: "+ HOST + " and PORT: ", PORT)
        while True:
            myserver.listen(1)
            conn, addr = myserver.accept()
            newclientthread = ClientThread(addr, conn)
            newclientthread.start()
            
    except Exception:
        print('Error occured')#print exception on user side
    finally:
        myserver.close()
#https://github.com/elisontuscano/Distributed-System-Client-Server-Directoy-Management