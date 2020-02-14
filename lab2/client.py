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

#append hmac to message, delimited by ";"
def hmac_digest(text, key_h):
    text = text.rstrip()
    h_1 = hmac.new(key_h, text.encode('utf-8'))
    return h_1.hexdigest()

def validate_message(text, digest, key_h):
    h_1 = hmac.new(key_h, text.encode('utf-8'))
    my_digest = h_1.hexdigest()
    print("Message: " + text)
    print("Digest: " + digest + "\n")
    print("My Digest: " + my_digest)
    print("Validated: " + str(hmac.compare_digest(digest, my_digest)))


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

key_d = DesKey(key_des.encode('utf-8'))
key_h = key_hmac.encode('utf-8')

print("DES key: ")
print(key_des.encode('utf-8'))
print("HMAC key: ")
print(key_h)
print()

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
            print("\n" + message[0].decode('utf-8'))
            message = message[1]
            print("Ciphertxet:")
            print(message)
            try:
                message = key_d.decrypt(message, padding=True)
            except:
                print("[Unable to decrypt message]")
                print(sys.exc_info()[0])
            else:
                message = message.decode('utf-8')
                message = message.split('\n')
                plaintext = message[0]
                digest = message[1]

                validate_message(plaintext, digest, key_h)
                print()
        else:
            plaintext = sys.stdin.readline()
            #hmac appended to plaintext message here
            digest = hmac_digest(plaintext, key_h)
            sys.stdout.write("\n<You>\n")
            sys.stdout.write("Plaintext:" + plaintext)
            sys.stdout.write("Digest:" + digest + "\n")
            message = plaintext + digest
            #des message encryption here
            message = key_d.encrypt(message.encode('utf-8'), padding=True)
            print("Ciphertext:" + str(message) + "\n")
            #print(message)
            server.send(message)
            sys.stdout.flush()
server.close()
