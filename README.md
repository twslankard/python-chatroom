Python UDP chatroom server
==========================

Copyright 2020 Tom Slankard

Overview
--------

This is just a toy example of a command-line chatroom, both client and server, implemented using Python. There is only one room, no protocol validation, and no user authentication. The sole purpose of this project was to learn a little about how UDP works, so I'm passing it along for others to use as an example.

The server and clients interact in a connectionless way. This means that they use the socket.sendto and socket.recvfrom methods to communicate. In these methods, the destination address and port are specified.

The protocol used to communicate from client to server and also from server to client is a simple JSON protocol that looks like this:

    {
      "username" : "foo",
      "message" : "hello, world",
      "color" : 32
    }

To run the server:

    python server.py [ip address] [port]

To run the client:

    python client.py [server ip address] [server port] [username] [color code]

The color code specifies what color your text will appear to others in the chat room. The color code follows the ANSI color standard for consoles, e.g. 31=red, 32=yellow, 33=green

Have fun!

Testing
-------

To run tests:

    pytest

Requirements
------------

* Python 3.6/3.7
* pytest

