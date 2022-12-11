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

    #Function run
    def run(self):
        while True:
            job = self.queue_in.get()
            if job is POISON_PILL:
                self.queue_in.put(POISON_PILL)
                break
            if plaintext := job(self.hash_value):
                self.queue_out.put(plaintext)
                break

#function main
def main(args):
    t1 = time.perf_counter
    queue_in = multiprocessing.Queue()
    queue_out = multiprocessing.Queue()

    workers = [
        Worker(queue_in, queue_out, args.hash_value)
        for _ in range(args.num_workers)
    ]

    for worker in workers:
        worker.start()

    for text_length in range(1, args.max_length + 1):
        combinations = Combinations(ascii_lowercase, text_length)
        for indices in chunk_indices(len(combinations), len(workers)):
            queue_in.put(Job(combinations, *indices))

    queue_in.put(POISON_PILL)

    while any(worker.is_alive() for worker in workers):
        try:
            solution = queue_out.get(timeout = 0.1)
            if solution:
                t2 = time.perf_counter()
                print(f"{solution} (found in {t2 - t1:.1f}s)")
                break
        except queue.Empty:
            pass
    else:
        print("Unable to find a solution")
        