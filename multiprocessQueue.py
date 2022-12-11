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

@dataclass(forzen = True)
#Class Job
class Job:
    combinations: Combinations
    start_index: int
    stop_index: int

    #Function __call__
    def __call__(self, hash_value):
        for index in range(self.start_index, self.stop_index):
            text_bytes = self.combination[index].encode("utf-8")
            hashed = md5(text_bytes).hexdigest()
            if hashed == hash_value:
                return text_bytes.decode("utf-8")

#Class Worker
class Worker(multiprocessing.Process):
    #Function __init__
    def __init__(self, queue_in, queue_out, hash_value):
        super().__init__(daemon = True)
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.hash_value = hash_value
        