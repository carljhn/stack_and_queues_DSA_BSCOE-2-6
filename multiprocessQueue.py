# Using multiprocessing.Queue for Interprocess Communication (IPC)

#Import libraries
import argparse
import multiprocessing
import queue
import time
from dataclasses import dataclass
from hashlib import md5
from string import ascii_lowercase

#Variable POISON_PILL
POISON_PILL = None

#Class named Combinations
class Combinations:
    #function __init__
    def __init__(self, alphabet, length):
        self.alphabet = alphabet
        self.length = length