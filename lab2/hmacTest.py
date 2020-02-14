# Python program to implement client side of chat room.
import socket
import select
import sys
import random
import string
import re

from des import DesKey
import hmac

key = 'aoeuaoeu'
key_h = hmac.new(key)

print(key)
print(key_h)

