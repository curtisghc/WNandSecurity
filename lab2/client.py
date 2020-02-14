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
#this function is called when sending a message
def hmac_digest(text, key_h):
    #strip newline from taking stdin
    text = text.rstrip()
    #create hmac object from key and plaintext
    h_1 = hmac.new(key_h, text.encode('utf-8'))
    #return only the hex encoded digest
    return h_1.hexdigest()

#check hmac validation, this is called by the reciever of a message
def validate_message(text, digest, key_h):
    #create hmac object
    h_1 = hmac.new(key_h, text.encode('utf-8'))
    my_digest = h_1.hexdigest()
    #original plaintext
    print("Message: " + text)
    #hex digest recieved from sender
    print("Digest: " + digest + "\n")
    #recievers own calculation of digest
    print("My Digest: " + my_digest)
    #compare the two, basically just a "=="
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

    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
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
server.close()
