#!/usr/bin/env python

import select
import socket
import os
import sys
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json


def get_messages(sock, epoll, username, color):
    while True:
        poll_result = epoll.poll()
        for event in poll_result:
            if event[1] == select.EPOLLIN:
                data, addr = sock.recvfrom( 1024, socket.MSG_DONTWAIT ) # buffer size is 1024 bytes

                #  parse the json from the server
                message = json.loads(data.decode())

                if message['username'] == username:
                    continue

                msg_str = message['message']

                #  if there is no user name, don't display it
                if message['username']:
                    msg_str = message['username'] + ": " + msg_str

                #  print the message, with colors if allowed
                if len(message['message']) > 0:
                    if allow_color:
                        print("\033[%sm%s\033[0m" % (message['color'], msg_str))
                    else:
                        print(msg_str)


def get_input(sock, username, color):
    while True:
        message = { "username" : username, "message" : input().strip(), "color" : color  }
        sock.sendto( json.dumps(message).encode(), (server_ip, int(server_port)) )


if __name__ == '__main__':

    server_ip = sys.argv[1].strip()
    server_port = sys.argv[2].strip()
    username = sys.argv[3].strip()

    color = 0
    allow_color = True
    try:
        color = sys.argv[4]
        if color == "--nocolor":
            allow_color = False
            color = "0"
    except:
        pass

    sock = socket.socket( socket.AF_INET, # Internet
                          socket.SOCK_DGRAM ) # UDP

    #  use epoll to wait for read events
    epoll = select.epoll()
    epoll.register(sock, select.EPOLLIN)

    thread.start_new_thread(get_input, (sock, username, color))
    thread.start_new_thread(get_messages, (sock, epoll, username, color))

    #  upon "connecting", send /hello and /who to announce our arrival and get a list
    #  of other people in the room
    message = { "username" : username, "message" : "/hello", "color" : color  }
    sock.sendto( json.dumps(message).encode(), (server_ip, int(server_port)) )
    message = { "username" : username, "message" : "/who", "color" : color  }
    sock.sendto( json.dumps(message).encode(), (server_ip, int(server_port)) )
    try: 
        while 1:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("bye")
        message = { "username" : username, "message" : "/goodbye", "color" : color  }
        sock.sendto( json.dumps(message).encode(), (server_ip, int(server_port)) )
        sys.exit(0)

