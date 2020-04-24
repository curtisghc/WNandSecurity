# Python program to implement client side of chat room.
import socket
import select
import sys
import random
import string
import re
import time
import math
import rsa
from des import DesKey


def read_key(fname):
    with open(fname, 'r') as fp:
        return fp.read()

print("Client process")

id_client = "ID-Client"
id_server = "ID-Server"
id_ca = "ID-CA"
req = "memo"

pubkey_ca = rsa.PublicKey.load_pkcs1(read_key("public_ca.pem"))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 2:
    print("Correct usage: client.py [server port]")
    exit()

k_tmp2_str = read_key("des_key_tmp2")
k_tmp2 = DesKey(k_tmp2_str.encode('utf-8'))

ip_address = "127.0.0.1"
server_port = int(sys.argv[1])

conn_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_s.connect((ip_address, server_port))

#Initial message to Server
ts_3 = str(time.time())
message = [id_server, str(ts_3)]
message = "@@@".join(message)
conn_s.send(message.encode('utf-8'))

#response from server
message = conn_s.recv(2048).decode("utf-8")
message = str.split(message, "@@@")
print("Response from server")
print(message)
print()

pub_server_str = message[0]
pub_key_server = rsa.PublicKey.load_pkcs1(pub_server_str)
cert_str = message[1]
cert = cert_str.encode("ISO-8859-1")
ts_4 = message[2]

#Verify Server's certificate
cert_plaintext = [id_server, id_ca, pub_server_str]
cert_plaintext = "$$$".join(cert_plaintext)
verified = rsa.verify(cert_plaintext.encode("ISO-8859-1"), cert, pubkey_ca)
if(verified):
    print("Server verified by CA")
else:
    print("Verification failed, closing connection and exiting")
    conn_s.close()
    quit()
print()


#message server to enstablish session key
ts_5 =  str(time.time())
message = [k_tmp2_str, id_client, ip_address, ts_5]
message = "@@@".join(message)
message = rsa.encrypt(message.encode("utf-8"), pub_key_server)
conn_s.send(message)

#recieve session key from server
message = conn_s.recv(2048)
message = k_tmp2.decrypt(message, padding=True)
message = message.decode("utf-8")
message = str.split(message, "@@@")
print("Session key recieved from Server:")
print(message)
print()
key_sess_str = message[0]
key_sess = DesKey(key_sess_str.encode("utf-8"))
lifetime_sess = int(message[1])

#message server with request for service
ts_7 = str(time.time())
message = [req, ts_7]
message = "@@@".join(message)
message = key_sess.encrypt(message.encode("utf-8"), padding=True)
conn_s.send(message)

#recieve data from server
message = conn_s.recv(2048)
message = key_sess.decrypt(message, padding=True)
message = message.decode("utf-8")
message = str.split(message, "@@@")
print("Data reciveed from server")
print(message)
print()
data = message[0]
ts_8 = float(message[1])

if(time.time() - ts_8 > lifetime_sess):
    print("Session key expired, closing connection")
    conn_s.close()
    quit()
else:
    print("Valid session key in data response")


conn_s.close()
quit()
