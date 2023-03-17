import math, requests, random
from random import *
from random_word import RandomWords

def getWords():
    r = RandomWords()
    ##get 64 random words
    message = ""
    for x in range(64):
        message += r.get_random_word()
        message += " "
    return message

print(getWords())
    