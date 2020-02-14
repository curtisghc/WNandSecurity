# Lab 2 for wireless networks and security

![Screenshot](https://raw.githubusercontent.com/curtisghc/Security_Lab_1/master/Screenshot.png)

## Dependencies
Currently Python2.7 and 3 are needed, will fix later.
Install DES library.
HMAC library is provided by python

```
sudo apt install python3-pip
sudo pip3 install des
```

## Usage
This package provides a server hosted chatroom, where messages are encrypted at endpoints using DES, and then the sender is validated using HMAC.

Keys can be generated at start, or provided in files, but the length of the DES key must be divisible by 8.
Keys are stored in the following files:
- DES key - "key_d.txt"
- HMAC key - "key_h.txt"

Run the server in python2 for now.
To run as a demo, use the loopback address and a random port number:
```
python server.py 127.0.0.1 9909
```

Then clients connect using the same ip and port number:
```
python3 client.py 127.0.0.1 9909
```

- Sent messages' plaintext will be displayed along with the HMAC digest and the ciphertext
- Recieved messages will be displayed as a cyphertext byte string, plaintext, and the two generated digests, one by the sender and one by the reciever, along with the validation status.


## Process
Upon sending a message:
1. Digest is generated using the plaintext and HMAC key
2. Digest is appended to plaintext
3. Message is encrypted using DES key
Upon message reception:
1. Ciphertext is decrypted using client's DES key
2. Plaintext and digest are separated
3. Second Digest is generated using the plaintext and the client's own HMAC key
4. Digests are compared to validate message


## Todo
- Port server file to Python 3
- Sometimes there's an error on decrypting depending on the message, but it doesn't trigger consistently
- Index out of bounds error when parsing the digest, related to extremely long messages

