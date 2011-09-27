#!/usr/bin/env python

import socket
import os
import sys
import thread
import time
import json

server_ip = sys.argv[1]
server_port = sys.argv[2]
username = sys.argv[3]

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


def get_messages():
  global sock, username, color
  while True:
    data = None
    try:
      data, addr = sock.recvfrom( 1024, socket.MSG_DONTWAIT ) # buffer size is 1024 bytes
    except socket.error:
      # wait a bit
      time.sleep(0.01)
    if data:
      #print data
      try:
        
        #  parse the json from the server
        message = json.loads(data)

        #  if the message is from us, then ignore it
        if(message['username'] != username):
          msg_str = message['message']

          #  if there is no user name, don't display it
          if(message['username']):
            msg_str = message['username'] + ": " + msg_str
      
          #  print the message, with colors if allowed
          if len(message['message']) > 0:
            if allow_color:
              print "\033[%sm%s\033[0m" % (message['color'], msg_str)
            else:
              print msg_str
      except ValueError:
        print "error: tried to decode something invald"

def get_input():
  global sock, username, color
  try:
    while True:
      #message = username + ": " + raw_input()
      #sock.sendto( message, (server_ip, int(server_port) ) )
      message = { "username" : username, "message" : raw_input().strip(), "color" : color  }
      sock.sendto( json.dumps(message), (server_ip, int(server_port)) )

  except KeyboardInterrupt:
    print "byebye now"

thread.start_new_thread(get_input, ())
thread.start_new_thread(get_messages, ())

#  upon "connecting", send /hello and /who to announce our arrival and get a list
#  of other people in the room
message = { "username" : username, "message" : "/hello", "color" : color  }
sock.sendto( json.dumps(message), (server_ip, int(server_port)) )
message = { "username" : username, "message" : "/who", "color" : color  }
sock.sendto( json.dumps(message), (server_ip, int(server_port)) )
try: 
  while 1:
    time.sleep(0.01)
except KeyboardInterrupt:
  print "bye"
  message = { "username" : username, "message" : "/goodbye", "color" : color  }
  sock.sendto( json.dumps(message), (server_ip, int(server_port)) )
  sys.exit(0)
