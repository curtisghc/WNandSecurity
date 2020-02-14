# Python program to implement client side of chat room.
import socket
import select
import sys
import random
import string
import re

from des import DesKey
import hmac


def keygen(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def write_key(key, fname):
    with open(fname, 'w') as fp:
        fp.write(key)
    print("Key written to \"" + fname + "\"")


def read_key(fname):
    with open(fname, 'r') as fp:
        return fp.read()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

should_generate = input("Generate new keys? (y/n)")

if (should_generate == "y"):
    key_des = keygen(8)
    key_hmac = keygen(8)
    write_key(key_des, "key_d.txt")
    write_key(key_hmac, "key_h.txt")
else:
    key_des = read_key("key_d.txt")
    key_hmac = read_key("key_h.txt")


print("DES key: ")
print(key_des.encode('utf-8'))
print("HMAC key: ")
print(key_hmac.encode('utf-8'))

key_d = DesKey(key_des.encode('utf-8'))
key_h = hmac.new(key_hmac.encode('utf-8'))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    """ There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            message = message.split(b' ')
            print("\nMessage from " + message[0].decode('utf-8'))
            print("Ciphertxet:")
            print(message[1])
            try:
                message[1] = key_d.decrypt(message[1], padding=True)
            except:
                print("[Unable't decrypt message from " + message[0] + "]")
            else:
                message[1] = message[1].decode('utf-8')
                print("Plaintext:")
                print(message[1])
        else:
            message = sys.stdin.readline()
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            message = key_d.encrypt(message.encode('utf-8'), padding=True)
            server.send(message)
            sys.stdout.flush()
server.close()
