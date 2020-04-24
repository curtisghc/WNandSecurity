# Python program to implement server side of chat room.
import socket
import select
import sys
import time
import math
import random
import string
from des import DesKey
import rsa

def read_key(fname):
    with open(fname, 'r') as fp:
        return fp.read()

def keygen(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Basic constants defined in lab manual
id_server = "ID-Server"
data = "take cis3319 class this afternoon"

print("Server process")

conn_ca = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print("Correct usage: server.py [server port] [ca port]")
    exit()

ip_address = "127.0.0.1"

# port number as argument
server_port = int(sys.argv[1])
ca_port = int(sys.argv[2])

"""
with open('public_ca.pem', 'rb') as fp:
    keydata = fp.read()
"""
pubkey_ca = rsa.PublicKey.load_pkcs1(read_key("public_ca.pem"))

#initial connection to CA
conn_ca.connect((ip_address, ca_port))

k_tmp1_str = read_key("des_key_tmp1")
k_tmp1 = DesKey(k_tmp1_str.encode("utf-8"))

ts_1 = str(time.time())

plaintext = [k_tmp1_str, id_server, ts_1]
plaintext = "@@@".join(plaintext)
ciphertext = rsa.encrypt(plaintext.encode("utf-8"), pubkey_ca)
conn_ca.send(ciphertext)

#response from CA
message = conn_ca.recv(2048)
message = k_tmp1.decrypt(message, padding=True).decode("utf-8")
message = str.split(message, "@@@")
print("Response from CA:")
print(message)
print()

pub_key_server_str = message[0]
pub_key_server = rsa.PublicKey.load_pkcs1(pub_key_server_str)
prv_key_server_str = message[1]
prv_key_server = rsa.PrivateKey.load_pkcs1(prv_key_server_str)
cert_str = message[2]
cert = cert_str.encode("ISO-8859-1")
ts_2 = message[4]

conn_ca.close()


#begin listening for client request
server.bind((ip_address, server_port))
server.listen(1)

conn_c, addr_c = server.accept()
message = conn_c.recv(2048)
message = message.decode("utf-8")
message = str.split(message, "@@@")
print("Initial request from Client:")
print(message)
print()

ts_3 = float(message[1])

#response to client
ts_4 = str(time.time())
message = [pub_key_server_str, cert_str, ts_4]
message = "@@@".join(message)
conn_c.send(message.encode("utf-8"))

#recieve session key from client
message = conn_c.recv(2048)
message = rsa.decrypt(message, prv_key_server)
message = message.decode("utf-8")
message = str.split(message, "@@@")
print("Request for session key recieved from client")
print(message)
print()
k_tmp2_str = message[0]
k_tmp2 = DesKey(k_tmp2_str.encode('utf-8'))
id_c = message[1]

#response to client with established session key
key_sess_str = read_key("des_key_sess")
key_sess = DesKey(key_sess_str.encode("utf-8"))
lifetime_sess = 1000
ts_6 = str(time.time())

message = [key_sess_str, str(lifetime_sess), id_c, ts_6]
message = "@@@".join(message)
message = k_tmp2.encrypt(message.encode("utf-8"), padding=True)
conn_c.send(message)

#recieve request for service from client
message = conn_c.recv(2048)
message = key_sess.decrypt(message, padding=True)
message = message.decode("utf-8")
message = str.split(message, "@@@")
print("Request for data from Client:")
print(message)
print()
req = message[0]
ts_7 = float(message[1])

#check lifetime of session for client
if(time.time() - ts_7 > lifetime_sess):
    print("Session key expired, closing connection")
    conn_c.close()
    quit()
else:
    print("Valid session key in data request")

#send data to client
ts_8 = str(time.time())
message = [data, ts_8]
message = "@@@".join(message)
message = key_sess.encrypt(message.encode("utf-8"), padding=True)
conn_c.send(message)


conn_c.close()
quit()
