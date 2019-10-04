# Created by Monalisa Sha
# Server.py : where server functions are written to communicate with the client and server.

import socket
import pickle
import random
import time
import sys
'''
TO DO:
- fix an syntax errors
-organize code
- get clients and server to connect

'''


bidTracker = {} #Dictionary to keep track of the bidding process Stored in {addr: Item Name} Format
clients = [] #Array to keep track of client information (socket obj, addr)
multiBid = {} #Dictionary that keeps track of items that are being bid on by multiple clinets {Item Name: [addr]}
itemData = {} #Stores item information taken from input file {ItemName: (units, max bid)}
winnerInfo = {} #stores record of items won {addr: [(itemName, amount owned)]}
notifD = "Default"


def getSocket(addr):
    global clients
    for i in range (0, len(clients)):
        if (clients[i][1]== addr):
            c = clients[i][0]
            return c

def itemWon(itemName, addr):
    win = "Server: Congratulations! You've won 1 " + itemName + ". "
    c = None
    global winnerInfo
    global itemData
    for i in range(0,len(clients)):
        if (clients[i][1]==addr):
            c = clients[i][0]
    c.send("Won".encode('utf-8'))
    time.sleep(.5)
    c.send(win.encode('utf-8'))
    time.sleep(.5)
    if addr in winnerInfo:
        ls = winnerInfo[addr]
        for i in range(len(ls)):
            if itemName in winnerInfo[addr][i]:
                tList = list(winnerInfo[addr][i])
                tList[1]+= 1
                winnerInfo[addr][i] = tuple(tList)
        ls.append((itemName, 1))
    if addr not in winnerInfo:
        winnerInfo[addr] = [(itemName, 1)]    
    tempList = list(itemData[itemName])
    tempList[0] -=1
    itemData[itemName] = tuple(tempList)

    tempList = list(itemData[itemName])
    itemList[0] = -1
    itemData[itemName] = tuple(tempList)

    if addr not in winnerInfo:
        winnerInfo[addr] = [(itemName, 1)]
        winnerInfo

def delValue():
    global multiBid
    global bidTracker
    tempList= []
    for key in bidTracker:
        if bidTracker[key] in multiBid:
            tempList.append(key)
    for i in range(0, len(tempList)):
        del bidTracker[tempList[i]]

def appendValue(dict, key, val):
    if key in dict:
        list= dict[key]
        if val not in list:
            dict[key].append(val)
    dict[key]= [val]

#Asks array of clients for their bids
def solicitBids():
    invite = "Server: You may now bid on an item. "
    global bidTracker
    global clients
    for i in range (0,len(clients)):
        c = clients[i][0]
        c.send(invite.encode('utf-8'))
        time.sleep(.5)
        temp = (c.recv(1024)).decode('utf-8', 'ignore')
        #Will Recv string Item Name and added into bids array
        print(clients[i][1])
        print(temp)
        bidTracker[clients[i][1]] = temp

#Checks for case where one item was bid on by more than 1 client, returns dict of items: [addr]
def checkMultBid():
    global multiBid
    global bidTracker
    for key in bidTracker:
       itemName = bidTracker[key]
       tempL = []
       if itemName not in multiBid:
            copyDict = bidTracker.copy()
            for k in copyDict:
                if itemName == copyDict[k]:
                    if key != k:
                        if key not in tempL:
                            tempL.append(key)
                        tempL.append(k)
            multiBid[itemName] = list(set(tempL))
    emptKey = []
    for key in multiBid:
        if multiBid[key]==[]:
            emptKey.append(key)
    for i in range(0,len(emptKey)):
        del(multiBid[emptKey[i]])

def bidWarMode(itemName, listAddr):
    itemWon(itemName, bidWarH(itemName, listAddr, 50, None))


#recursive call that keeps bid war going, returns addr of person who won
def bidWarH(itemName, listAddr, price, leader):
    global clients
    newPrice = price+1
    notifW = "Winning"
    notifO = "Outbid"
    losing = "Server: You have been outbid by another client, submit a new bid or lose the item. The price to beat is: $" + str(price+1) + ". "
    winning = "Server: You are currently winning the bid with a price of $" + str(newPrice) + ". "
    lost = "Server: I'm sorry but you did not win " + itemName + ". "
    if (newPrice >= itemData[itemName][1]):
        if clients[i][0] in listAddr:
                clients[i][0].send(lost.encode('utf-8'))
                time.sleep(.5)
        return leader
    nleader = listAddr[random.randint(0,len(listAddr)-1)]
    listAddr.remove(nleader)
    if (leader != None):
        listAddr.append(leader)
    newBids = []
    for i in range(0, len(clients)):
        if (clients[i][1] == nleader):
            clients[i][0].send(notifW.encode('utf-8'))
            time.sleep(.5)
            clients[i][0].send(winning.encode('utf-8'))
            time.sleep(.5)
        elif clients[i][1] in listAddr:
            clients[i][0].send(notifO.encode('utf-8'))
            time.sleep(.5)
            clients[i][0].send(losing.encode('utf-8'))
            time.sleep(.5)
            clients[i][0].send(pickle.dumps(newPrice))
            time.sleep(.5)
            np = clients[i][0].recv(1024)
            if (pickle.loads(np) == newPrice+1):
                newBids.append(clients[i][1])
            else:
                clients[i][0].send(lost.encode('utf-8'))
                time.sleep(.5)
    if (newBids == []):
        return nleader
    else: bidWarH(itemName, newBids, newPrice, nleader)



s = socket.socket()
port = 12345
s.bind(('', port))
print("Looking for Clients")
s.listen(5)

#intializes array of clients
for i in range(0,3):
    c, addr = s.accept()
    clients.append((c,addr))
    print('Connected to: ', addr)

#Block for Data Collection from file
f = open("input.txt", "r")
flines = f.readlines()
for i in range(1,len(flines)):
    nline = flines[i].split()
    itemData[nline[0]] = [int(nline[1]), int(nline[2])] #Puts data in dictionary organized by {"Item Name":[Units,Price]} for updating and reading
print(itemData)
f.close()

#loop until input, once ended transmit all items in winnerInfo
while True:
    try:
        for i in range(0,len(clients)):
            c = clients[i][0]
            print('Sending Item Data to: ', clients[i][1])
            c.send(pickle.dumps(itemData))
            time.sleep(.5)
        solicitBids()
        checkMultBid()
        delValue()
        for key in bidTracker:
            z = getSocket(key)
            z.send(notifD.encode('utf-8'))
            time.sleep(.5)
            z.send("Server: No one else has bid on your item.".encode('utf-8'))
            time.sleep(.5)
            itemWon(bidTracker[key],key)
            for key in multiBid:
                bidWarMode(key, multiBid[key])
        multiBid.clear()
        bidTracker.clear()
    except KeyboardInterrupt:
        print("Bidding Ended. Here are the Results: ")
        print(winnerInfo)
        sys.exit()
