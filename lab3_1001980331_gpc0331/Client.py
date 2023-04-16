#GLEN CORREIA
#1001980331
import socket
import sys
from threading import Lock
import tkinter as tk
import re
import os
from os import path
import os.path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def setup():
    #https://realpython.com/python-sockets/
    myclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    myclient.connect((HOST, PORT))
    return myclient, HOST, PORT

class Handler(FileSystemEventHandler):
    def create(self,event):
        print("File create"+ event.src_path) #printing the created file

    def delete(self,event):
        print("File delete"+ event.src_path) #printing the deleted file

    def modi(self,event):
        print("File modi"+ event.src_path) #printing the modified file

if __name__ == "__main__":

    HOST = '127.0.0.1'
    PORT = 9090

    observer = Observer() #create observer
    event_handler = Handler() #create handler
    observer.schedule(event_handler, "A_dir", recursive = False) #schedule handler
    observer.start()

    myclient, HOST, PORT = setup()  #GETTING SETUP DETAILS
    USER_STATUS =True 
    print(str("Client connected"))
    
    

    while USER_STATUS != False:
        pac = input("User@client:~$")
        pac = str(pac).split("-")

        print(pac)
        
        if len(pac) == 1: 
            if pac[0].strip() == 'lab3':
                myclient.send(str.encode(str("lab3")))  
                print("ServerA Connected")
                
                pi = str(myclient.recv(1024),'utf-8')
                res = eval(pi)
                print(type(res))
                for index, job in enumerate(res):
                        

                    print(f"[{index}]               {job}")

        else:
#Locking the file
            if pac[1].strip() == 'lock' :
                send_string = "lock -"+pac[2].strip()  
                myclient.send(str(send_string).encode())
                print ("File lock data sent")
#unLocking the file
            elif pac[1].strip() == "unlock":
                send_string = "unlock -"+pac[2].strip()  
                myclient.send(str(send_string).encode())
                print ("File unlock data sent")
                
 #exit condition               
            if pac == "exit":
                USER_STATUS = False
                sys.exit(0)
                break   

