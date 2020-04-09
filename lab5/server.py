# Python program to implement server side of chat room.
import socket
import select
import sys
import time
import math
import random
import string
from des import DesKey

def read_key(fname):
    with open(fname, 'r') as fp:
        return fp.read()

def keygen(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Basic constants defined in lab manual
id_tgs = "CIS3319TGSID"
id_v = "CIS3319SERVERID"

lifetime2 = "60"
lifetime4 = "86400"

key_c = DesKey(read_key("key_c").encode("utf-8"))
key_tgs = DesKey(read_key("key_tgs").encode("utf-8"))
key_v = DesKey(read_key("key_v").encode("utf-8"))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 2:
    print("Correct usage: server.py  [port number]")
    exit()

ip_address = "127.0.0.1"

# port number as argument
v_port = int(sys.argv[1])

print("This is the server process")
print("Listening on 127.0.0.1:"+ str(v_port) + "\n")

server.bind((ip_address, v_port))

server.listen(2)

# TGS and client must connect to server
conn_c, addr_c = server.accept()
conn_tgs, addr_tgs = server.accept()

# Recieve ticket from TGS for client
message = conn_tgs.recv(2048)
message = key_v.decrypt(message, padding=True).decode("utf-8")
message = str.split(message, "@@@")
k_cv = message[0]
id_c = message[1]
ad_c = message[2]
id_v = message[3]
timestamp4 = float(message[4])
lifetime4 = float(message[5])
print("Ticket recieved from TGS:")
print(message)
print()

# Recieve initial message from client and process
message = conn_c.recv(2048).decode("utf-8")
message = str.split(message, "@@@")
print("Message recieved Client -> V")
print(message)

# Check validity of Client's ticket
valid = False
print("Time delay: " + str(time.time() - timestamp4))
if(time.time() - timestamp4 < lifetime4):
    print("Client ticket is valid")
    valid = True
else:
    print("Client ticket is invalid")


# Process message to respond to client
message = str(time.time() + 1.0)
conn_c.send(message.encode("utf-8"))



"""

print("Message Client -> AS:")
print(message + "\n")
message = str.split(message, "@@@")
id_c = message[0]
timestamp1 = message[2]

# Processing for response message
key_ctgs = keygen()
timestamp2 = str(int(math.floor(time.time())))
ad_c = addr_c[0] + ":" + str(addr_c[1])

ticket_tgs = [key_ctgs, id_c, ad_c, id_tgs, timestamp2, lifetime2]
ticket_tgs = "@@@".join(ticket_tgs)
#ticket_tgs = key_tgs.encrypt(ticket_tgs.encode('utf-8'), padding=True)

message = [key_ctgs, id_tgs, timestamp2, lifetime2, ticket_tgs]
message = "@@@".join(message)
#message = key_c.encrypt(message.encode('utf-8'), padding=True)

conn_c.send(message.encode("utf-8"))

# Recieve message to TGS from Client
message = conn_c.recv(2048)
message = str.split(message, "@@@")
print("Message sent Client -> TGS")
print(message)

# Validate message
timestamp2 = int(message[5])
lifetime2 = int(message[6])
valid = False
if(int(math.floor(time.time())) - timestamp2 < lifetime2):
    print("Client ticket is valid")
    valid = True
else:
    print("Client ticket is invalid")

# Processing ticket for V
timestamp4 = str(int(math.floor(time.time())))
key_cv = keygen()
ad_c = addr_c[0] + ":" + str(addr_c[1])
ticket_v = [key_cv, id_c, ad_c, id_v, timestamp4, lifetime4]

# Processing response to client
message = [key_cv, id_v, timestamp4, "@@@".join(ticket_v)]
message = "@@@".join(message)
conn_c.send(message.encode("utf-8"))
"""


conn_c.close()
#conn_v.close()
server.close()

