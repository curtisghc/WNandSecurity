# Python program to implement client side of chat room.
import socket
import select
import sys
import random
import string
import re

from des import DesKey
import hmac

plainText = "the quick brown fox"

key_h = 'aoeuaoeu'

print(key)
print(key_h)

h1 = hmac.new(key, plainText)
h2 = hmac.new(key, plainText)

print(h1.hexdigest())
print(h2.hexdigest())

