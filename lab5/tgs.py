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
if len(sys.argv) != 3:
    print("Correct usage: tgs.py  [port number] [v port]")
    exit()

ip_address = "127.0.0.1"

# port number as argument
tgs_port = int(sys.argv[1])
v_port = int(sys.argv[2])

server.bind((ip_address, tgs_port))

server.listen(1)

print("This is the AS/TGS process")
print("Listening on 127.0.0.1:" + str(tgs_port) + "\n")

# V server and client must connect to TGS
conn_c, addr_c = server.accept()

# Recieve initial message from client and process
message = conn_c.recv(2048).decode("utf-8")
message = str.split(message, "@@@")
print("Message recieved Client -> AS:")
print(message)
print("\n")
id_c = message[0]
timestamp1 = message[2]

# Processing for response message
k_ctgs = keygen()
key_ctgs = DesKey(k_ctgs.encode("utf-8"))
timestamp2 = str(time.time())
ad_c = addr_c[0] + ":" + str(addr_c[1])

ticket_tgs = [k_ctgs, id_c, ad_c, id_tgs, timestamp2, lifetime2]
ticket_tgs = "@@@".join(ticket_tgs)
ticket_tgs = key_tgs.encrypt(ticket_tgs.encode('utf-8'), padding=True)
ticket_tgs = ticket_tgs.decode("ISO-8859-1")

message = [k_ctgs, id_tgs, timestamp2, lifetime2, ticket_tgs]
message = "@@@".join(message)
message = key_c.encrypt(message.encode('utf-8'), padding=True)

conn_c.send(message)
#conn_c.send(message.encode("utf-8"))



""" TGS processes start here"""


# Recieve message to TGS from Client
message = conn_c.recv(2048).decode("utf-8")
message = str.split(message, "@@@")
ticket_tgs = message[1].encode("ISO-8859-1")
ticket_tgs = key_tgs.decrypt(ticket_tgs, padding=True).decode("utf-8")
ticket_tgs = str.split(ticket_tgs, "@@@")

print("Message recieved Client -> TGS")
print(message)
print("Decrypted TGS ticket from client:")
print(ticket_tgs)

# Validate message
timestamp2 = float(ticket_tgs[4])
lifetime2 = float(ticket_tgs[5])
valid = False
print("Time delay: " + str(time.time() - timestamp2))
if(time.time() - timestamp2 < lifetime2):
    print("Client ticket is valid")
    valid = True
else:
    print("Client ticket is invalid")

# Processing ticket for V
timestamp4 = str(time.time())
k_cv = keygen()
ad_c = addr_c[0] + ":" + str(addr_c[1])
ticket_v = [k_cv, id_c, ad_c, id_v, timestamp4, lifetime4]
ticket_v = "@@@".join(ticket_v)
ticket_v = key_v.encrypt(ticket_v.encode("utf-8"), padding=True)

# Send ticket to v
server_v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_v.connect((ip_address, v_port))
server_v.send(ticket_v)

# Processing response to client
ticket_v = ticket_v.decode("ISO-8859-1")
message = [k_cv, id_v, timestamp4, ticket_v]
message = "@@@".join(message)
message = key_ctgs.encrypt(message.encode("utf-8"), padding=True)
conn_c.send(message)

conn_c.close()
server_v.close()
server.close()

