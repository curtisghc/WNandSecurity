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

def write_key(fname, key):
    with open(fname, 'w') as fp:
        fp.write(key)

def read_key(fname):
    with open(fname, 'r') as fp:
        return fp.read()

def keygen(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Basic constants defined in lab manual
id_ca = "ID-CA"

#rsa key generation
(pubkey_ca, privkey_ca) = rsa.newkeys(512)

write_key("public_ca.pem", pubkey_ca.save_pkcs1().decode('utf-8'))
print("RSA key generated, public key written to \"public_ca.pem\"")

#key_v = DesKey(read_key("key_v").encode("utf-8"))

ca = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ca.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 2:
    print("Correct usage: tgs.py  [ca port number]")
    exit()

ip_address = "127.0.0.1"

# port number as argument
ca_port = int(sys.argv[1])

ca.bind((ip_address, ca_port))

ca.listen(1)

print("CA process")
print("Listening on 127.0.0.1:" + str(ca_port) + "\n")

# server must connect to TGS
conn_s, addr_s = ca.accept()

# application server registration
message = conn_s.recv(2048)
message = rsa.decrypt(message, privkey_ca)
message = message.decode('utf-8')

message = str.split(message, "@@@")
print("Message recieved Server -> CA:")
print(message)
print("\n")
k_tmp1_str = message[0]
k_tmp1 = DesKey(k_tmp1_str.encode("utf-8"))
id_server = message[1]
timestamp1 = message[2]

#response to server
(pub_server, prv_server) = rsa.newkeys(512)
pub_server_str = pub_server.save_pkcs1().decode("utf-8")
prv_server_str = prv_server.save_pkcs1().decode("utf-8")

cert = [id_server, id_ca, pub_server_str]
cert = "$$$".join(cert)

#rsa signature, should be decoded with  ISO-8859-1 rather than utf-8 for reasons
cert = rsa.sign(cert.encode("utf-8"), privkey_ca, 'SHA-1')
cert = cert.decode("ISO-8859-1")

ts_2 = str(time.time())

message = [pub_server_str, prv_server_str, cert, id_server, ts_2]
message = "@@@".join(message)
print(message)
message = k_tmp1.encrypt(message.encode("utf-8"), padding=True)
conn_s.send(message)

conn_s.close()
quit()

