# Python program to implement client side of chat room.
import socket
import select
import sys
import random
import string
import re
import time
import math
from des import DesKey


def read_key(fname):
    with open(fname, 'r') as fp:
        return fp.read()

print("This is the client process \n")

id_c = "CIS3319USERID"
id_tgs = "CIS3319TGSID"
id_v = "CIS3319SERVERID"

server_v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tgs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Correct usage: client.py [server port] [tgs port]")
    exit()

key_c = DesKey(read_key("key_c").encode('utf-8'))

ip_address = "127.0.0.1"
tgs_port = int(sys.argv[1])
v_port = int(sys.argv[2])

server_tgs.connect((ip_address, tgs_port))
server_v.connect((ip_address, v_port))

#Initial message to AS
timestamp1 = time.time()
message = [id_c, id_tgs, str(timestamp1)]
message = "@@@".join(message)
server_tgs.send(message.encode('utf-8'))

# Parse AS response
message = server_tgs.recv(2048)
message = key_c.decrypt(message, padding=True).decode("utf-8")
message = str.split(message, "@@@")

key_ctgs = DesKey(message[0].encode("utf-8"))
ticket_tgs = message[4]

print("\nMessage recieved AS -> Client:")
print(message[:4])
print("TGS ticket recieved:")
#To print escape characters
#print(ticket_tgs.encode("utf-8"))
print(ticket_tgs)
print()

# Client generates authenticator
timestamp3 = str(time.time())
authenticator_c = [id_c, timestamp3]

# Encrypt authenticator using client/tgs key
_authenticator_c = key_ctgs.encrypt("@@@".join(authenticator_c).encode("utf-8"), padding=True)
_authenticator_c = _authenticator_c.decode("ISO-8859-1")
#authenticator_c = "".join(chr(x) for x in authenticator_c)

# Client sends message with authenticator to TGS (same server as AS)
message = [id_v, ticket_tgs, _authenticator_c]
message = "@@@".join(message)
server_tgs.send(message.encode("utf-8"))

# Recieve decrypt, and process message from TGS
message = server_tgs.recv(2048)
message = key_ctgs.decrypt(message, padding=True).decode("utf-8")
message = str.split(message, "@@@")
k_cv = message[0]
key_cv = DesKey(k_cv.encode("utf-8"))

ticket_v = message[3]

print("\nMessage recieved TGS -> Client:")
print(message[:3])
print("Server ticket recieved:")
print(ticket_v)
print()

# Generate message to send to server
# Encrypt authenticator using client/server key
_authenticator_c = key_cv.encrypt("@@@".join(authenticator_c).encode("utf-8"), padding=True)
_authenticator_c = _authenticator_c.decode("ISO-8859-1")
message = [ticket_v, _authenticator_c]
message = "@@@".join(message)
server_v.send(message.encode("utf-8"))

# Recieve final message from server
message = server_v.recv(2048).decode("utf-8")
print("Message recieved V -> Client")
print(message)





"""
while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server_tgs]


    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])


    for socks in read_sockets:
        if socks == server_tgs:
            message = socks.recv(2048)
            message = message.split(b' ')
            #strip sender ip
            print("\n" + message[0].decode('utf-8'))
            message = message[1]
            #print base ciphertext
            print("Ciphertxet:")
            print(message)
            try:
                #decrypt entire message here
                message = key_d.decrypt(message, padding=True)
            except:
                #weird error
                print("[Unable to decrypt message]")
                print(sys.exc_info()[0])
            else:
                message = message.decode('utf-8')
                #newline delimits the end of plaintext and start of digest
                message = message.split('\n')
                plaintext = message[0]
                digest = message[1]

                #send message, digest, and secret key to validate
                validate_message(plaintext, digest, key_h)
                print()
        else:
            plaintext = sys.stdin.readline()
            #hmac generated from key and plaintext
            digest = hmac_digest(plaintext, key_h)

            sys.stdout.write("\n<You>\n")
            sys.stdout.write("Plaintext:" + plaintext)
            sys.stdout.write("Digest:" + digest + "\n")
            #hmac appended to plaintext
            message = plaintext + digest

            #des encrypts entire message here
            message = key_d.encrypt(message.encode('utf-8'), padding=True)
            print("Ciphertext:" + str(message) + "\n")
            server.send(message)
            sys.stdout.flush()
"""
server_tgs.close()
server_v.close()
