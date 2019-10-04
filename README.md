# e-Bidding
A e-bidding system using socket programming in python

Simple server-client program usimg python.

Here the server file have server program to connect

Server File: 
1.A server has a bind() method which binds it to a specific ip and port so that it can listen to incoming requests on 
that ip and port. 
2.A server has a listen() method which puts the server into listen mode. 
3.This allows the server to listen to incoming connections. And last a server has an accept() and close() method. 
4.The accept method initiates a connection with the client and the close method closes the connection with the client.

Server.py has all bidding related information like bidwar information , item won by the client etc.

Client File:
1. Server can interact with the client.
2. Client fike has the information of item choose by the client.

Item file:
It has all items data available for bidding and their prices.
