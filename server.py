#coding=utf-8
import socket 
import threading
import sys
import os 
import random
import time as my
# checks whether sufficient arguments have been provided
if (len(sys.argv)!=3):
    print "Correct usage: script, IP address, port number"
    exit()


server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# binds the server to an entered IP address(sys.argv[1]) and port number(sys.argv[2]) at the specified port number
server_socket.bind((sys.argv[1],int(sys.argv[2])))

# listens for 3 active connections
server_socket.listen(3)

# list of (conn,address)
list_conn=[]

# dictionary with keys as (conn,address) and value as time of recieving response from corrosponding connection
time1={}

# dictonary with keys as (conn,address) and values as score of corrosponding connection
scoreboard={}

# list storing questons and answers
questions=[("Who invented periodic table?","Dmitri Mendeleev"),("What is sodium chloride?","Table Salt"),("Solve 12+9=?","21"),("50 times 5 is equal to?","250"),("Simplify: 26 + 32 - 12","46"),("Solve : (24 + 4) ÷ 4","7"),("The person who works for free?","Volunteer"),("The disease bronchitis is associated with?","Lungs"),("The Ozone layer lies in the?","Stratosphere"),("Orkut.com is now owned by ?","Google"),("What is the national game of India?","Hockey"),("2010 Commonwealth Games held in ?","India"),("In 1924 the first winter Olympics was held in ?","France"),("H2O is the chemical formula for what?","Water"),("What is the capital of India","New Delhi"),("Which planet is the closest to Earth?","Venus"),("How many sides does an octagon have?","8"),("What is the top colour in a rainbow?","Red"),("What is the next prime number after (3)?","5"),("What is the square root of 36?","What is the square root of 36?")]
questions_order=range(20)
random.shuffle(questions_order)


def min_t(l):
    for i in range(3):
        if(list_conn[i]!=l and time1[l]>time1[list_conn[i]]):
            return 0
    return 1
   

# main function of controlling game using threading
def client_thread(conn,addr):
    conn.send("Welcome to TV game\n")
    conn.send("Game starts\n")
    conn.send("Instructions\n")
    conn.send("1-If the answer is correct, player will get 1 point, otherwise 0")
    conn.send("2- Game will be over if any of the player gets 5 points and will be declared the winner\n")
    conn.send("3-Player who presses the buzzer first will get a chance to see and answer the question")
    conn.send("4-To press buzzer select any key then press enter\n")
    conn.send("Press buzzer")
    while(1):
        time1[(conn,addr)]=float('inf')
        if(len(questions_order)==0):
            for i in loc:
                i[0].send("Game Over!")
                i[0].send("quit")
            exit()
        data=conn.recv(1024)
        print (my.localtime().tm_min)
        time1[(conn,addr)]=(int(my.localtime().tm_min)*60)+int(my.localtime().tm_sec)

        if(min_t((conn,addr))):
            print min_t((conn,addr))
            conn.send(questions[questions_order[len(questions_order)-1]][0])
            answer=conn.recv(1024)
            if(answer==questions[questions_order[len(questions_order)-1]][1]):
                scoreboard[(conn,addr)]=scoreboard[(conn,addr)]+1
            questions_order.pop()
            for i in list_conn:
                i[0].send("Points :- Player1={} Player2={} Player3={}\n".format(scoreboard[list_conn[0]],scoreboard[list_conn[1]],scoreboard[list_conn[2]]))
                i[0].send("Press Buzzer\n")

        if(scoreboard[list_conn[0]]==5):
            for i in list_conn:
                i[0].send("Player1 is Winner\n")
                i[0].send("Game over\n")
                i[0].send("quit")
            sys.exit()
        elif(scoreboard[list_conn[1]]==5):
            for i in list_conn:
                i[0].send("Player2 is Winner\n")
                i[0].send("Game over\n")
                i[0].send("quit")
            sys.exit()
        elif(scoreboard[list_conn[2]]==5):
            for i in list_conn:
                i[0].send("Player3 is Winner\n")
                i[0].send("Game over\n")
                i[0].send("quit")
            sys.exit()

for i in range(3):
    conn,addr=server_socket.accept()
    list_conn.append((conn,addr))
    time1[(conn,addr)]=float("inf")
    scoreboard[(conn,addr)]=0

for i in range(3):
    t=threading.Thread(target=client_thread,args=[list_conn[i][0],list_conn[i][1]])
    t.start()

