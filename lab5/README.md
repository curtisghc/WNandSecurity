# Lab 5:
## Kerberos version 4 implementation

This lab implements a Kerberos Authentication and Ticket Granting services to validate a client's connection to a server.
The AS and TGS are implemented in the same file "tgs.py", while the client and server are in their self-named Python files.

This project uses Python 3 and a number of libraries.
Python's socket programming is easy to use for IPC, and I did not use multi-threading to maintain multiple connections.

The only external library I used was the DesKey library for excrypting the messages.

No IDE was used to test this, simply a text editor and terminal emulators.


To run this program, first the server.py file must be run with its own port number as an argument, opening connection for the TGS and client:

`python3 server.py [server port]`

Then the TGS can run, where argument are its own port, and the server port to connect to:

`python3 tgs.py [tgs port] [server port]`

Finally, the client will run, where communications are hard coded, and there is no input:

`python3 client.py [tgs port] [server port]`

An example print out screen is provided in this folder.
