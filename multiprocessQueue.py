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

    #function __len__
    def __len__(self):
        return len(self.alphabet) ** self.length

    #function __getitem__
    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        return "".join(
            self.alphabet[
                (index // len(self.alphabet) ** i) % len(self.alphabet)
            ]
            for i in reversed(range(self.length))
        )