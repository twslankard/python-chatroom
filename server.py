#!/usr/bin/env python
'''
Copyright 2020 Tom Slankard
server usage:
python server.py [ip address] [port]
'''

import socket
import time
import sys
import json
import select
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def send(sock, data, clients):
    """
    Sends the specified message to each client in the clients list.
    """
    for client in clients:
        sock.sendto(data.encode(), client[1])


def create_response(message_json, client, clients):
    """
    Interprets the message from the client and responds accordingly,
    sending the message to other clients when appropriate.
    """  
    #  the /hello message_json announces the new client
    if( message_json['message'].startswith("/hello") ):
        return {"username" : "server",\
            "message" : message_json['username'] + " joined the chat",\
            "color" : 35 },\
            clients

    #  the /who message is only echoed back to the client who sent it
    #  The response is a list of other people in the chat room
    elif ( message_json['message'].startswith("/who") ):
        return {"username" : "server",\
            "message" : "people in room: " + ', '.join([y[0] for y in clients]),\
            "color" : 35 },\
            [client]

    #  The /goodbye message let's everyone know we're leaving
    elif ( message_json['message'].startswith("/goodbye") ):
        clients.remove(client)
        return {"username" : "server",\
            "message" : message_json['username'] + " left the chat",\
            "color" : 35 },\
            clients

    #  The /me message creates an "emote"
    elif ( message_json['message'].startswith("/me") ):
        newmsg = message_json['username'] + message_json['message'][3:]
        return {"username" : None, "message" : newmsg, "color" : message_json['color'] },\
            clients

    #  All other messages are simply re-sent back to all clients
    return {"username" : message_json['username'],\
        "message" : message_json['message'],\
        "color" : message_json['color'] },\
        clients
    

def handle_client_data(data, addr, clients):
    """Handles a message read from a new or existing client."""
    message_json = json.loads(data)
    client = (message_json['username'], addr)
    if client not in clients:
        clients.append(client)

    if data:
        response, clients = create_response(message_json, client, clients)
        send(sock, json.dumps(response), clients)


def wait_for_message_and_respond(sock, epoll, clients):
    """Waits for a message and processes it."""
    poll_result = epoll.poll()
    for event in poll_result:
        if event[1] == select.EPOLLIN:
            data, addr = sock.recvfrom( 1024, socket.MSG_DONTWAIT ) # buffer size is 1024 bytes
            logger.debug(data)
            logger.debug(clients)
            handle_client_data(data, addr, clients)


if __name__ == '__main__':
    """
    Creates a socket and epoll object for monitoring it,
    then handles messages on the socket forever.
    """
    UDP_IP=sys.argv[1]
    UDP_PORT=int(sys.argv[2])

    #  create a datagram socket 
    sock = socket.socket( socket.AF_INET, # Internet
                          socket.SOCK_DGRAM ) # UDP

    #  bind the socket to a port, to allow people to send info to it
    sock.bind( (UDP_IP,UDP_PORT) )

    #  use epoll to wait for read events
    epoll = select.epoll()
    epoll.register(sock, select.EPOLLIN)

    clients = []
    while True:
        wait_for_message_and_respond(sock, epoll, clients)
