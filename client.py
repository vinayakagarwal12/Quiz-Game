import socket
import sys
import os
import threading,time

# checks whether sufficient arguments have been provided
if (len(sys.argv)!=3):
    print "Correct usage: script, IP address, port number"
    exit()
    
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((sys.argv[1],int(sys.argv[2])))

# function for receiving message
def Receive():
    print client_socket.recv(50)
    while (1):
        try:
            message=client_socket.recv(1024)
            print message
            # terminate program when message = quit
            if(message=="quit"):
                sys.exit()
        except:
            continue
        
# function for sending message
def Send():
    while (1):
        try:
            message=raw_input()
            client_socket.send(message)
        except:
            continue
   
# receiving thread
receive=threading.Thread(target=Receive)

#sending thread
send=threading.Thread(target=Send)

receive.start()
send.start()
receive.join()
send.join()
