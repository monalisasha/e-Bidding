# Created by Monalisa Sha
# Client.py : where all client related functions are written to start the bidding.

import socket
import sys
import random
import pickle
import time

willBid = "We will bid on "

#Function that returns a Bool to determine whether to bid on item or not
def probBid():
    chance = random.randint(0,100)
    return(chance >= 0 and chance <= 33)

#Accepts a dictionary and randomly selects an item to bid
def chooseItem(dict):
    listKeys = list(dict.keys())
    return listKeys[random.randint(0,9)] #returns random item name to be bid on

s = socket.socket()
port = 12345
s.connect(('10.0.0.97', port))
print('Connected to Server')
while True:
    data = s.recv(1024)
    itemData = pickle.loads(data)
    itemName = chooseItem(itemData)
    print((s.recv(1024)).decode('utf-8', 'ignore'))
    print(willBid + itemName+ ". ")
    s.send(itemName.encode('utf-8'))
    l = True
    while (l):
        choice =(s.recv(1024)).decode('utf-8', 'ignore')
        if (choice == "Outbid"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
            np = s.recv(1024)
            newPrice = pickle.loads(np) + 1
            if (probBid()):
                print("Submitted new bid of: " + str(newPrice))
                s.send(pickle.dumps(newPrice))
                time.sleep(.5)
            else:
                print("Did not submit another bid.")
                s.send(pickle.dumps(1))
                time.sleep(.5)
                print((s.recv(1024)).decode('utf-8', 'ignore'))
                l = False

        elif(choice == "Lost"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
        elif(choice == "Winning"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
        elif(choice == "Won"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
            l = False
        elif(choice == "Default"):
            print((s.recv(1024)).decode('utf-8', 'ignore'))
        else: l = False
    itemData.clear()
s.close()
