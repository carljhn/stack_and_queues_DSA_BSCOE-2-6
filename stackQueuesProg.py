# Now suppose you’ve written a program with more than one flow of execution. Beyond being a valuable algorithmic tool, queues can help 
# abstract away concurrent access to a shared resource in a multithreaded environment without the need for explicit locking. 
# Python provides a few synchronized queue types that you can safely use on multiple threads to facilitate communication between them.

# In this section, you’re going to implement the classic multi-producer, multi-consumer problem using Python’s thread-safe queues. 
# More specifically, you’ll create a command-line script that lets you decide on the number of producers and consumers, their relative
# speed rates, and the type of queue:

import argparse
import threading
from dataclasses import dataclass, field 
from enum import IntEnum
from itertools import zip_longest
from queue import LifoQueue, PriorityQueue, Queue
from random import choice, randint
from time import sleep

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel

QUEUE_TYPES = {"fifo": Queue, "lifo": LifoQueue, "heap": PriorityQueue}

PRODUCTS = {
    ":balloons:", 
    ":cookies:", 
    ":crystal_ball:", 
    ":diving_mask:", 
    ":flashlight:", 
    ":gem:", 
    ":gift:", 
    ":kite:", 
    ":party_popper:", 
    ":postal_horn:", 
    ":ribbon:", 
    ":rocket:", 
    ":teddy_bear:", 
    ":thread:", 
    ":yo-yo:", 
}

@dataclass(order=True)

#Class Product
class Product:
    priority: int
    label: str = field(compare=False)

    def __str__(self):
        return self.label

#Class Priority(IntEnum)
class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

PRIORITIZED_PRODUCTS = {
    Product(Priority.HIGH, ":1st_place_medal:"),
    Product(Priority.MEDIUM, ":2nd_place_medal:"),
    Product(Priority.LOW, ":3rd_place_medal:"),
}

#Class Worker
class Worker(threading.Thread):
    def __init__(self, speed, buffer):
        super().__init__(daemon=True)
        self.speed = speed
        self.buffer = buffer
        self.product = None
        self.working = False
        self.progress = 0

    @property

    #function state
    def state(self):
        if self.working:
            return f"{self.product} ({self.progress}%)"
        return ":zzz: Idle"

    #function simulate_idle
    def simulate_idle(self):
        self.product = None
        self.working = False
        self.progress = 0
        sleep(randint(1, 3))

    #function simulate_work
    def simulate_work(self):
        self.working = True
        self.progress = 0
        delay = randint(1, 1 +15 // self.speed)
        for _ in range(100):
            sleep(delay / 100)
            self.progress += 1

#Class Producer 
class Producer(Worker):
    def __init__(self, speed, buffer, products):
        super().__init__(speed, buffer)
        self.products = products 

    def run(self):
        while True:
            self.product = choice(self.products)
            self.simulate_work()
            self.buffer.put(self.product)
            self.simulate_idle()

#Class Consumer 
class Consumer(Worker):
    def run(self):
        while True:
            self.product = self.buffer.get()
            self.simulate_work()
            self.buffer.task_done()
            self.simulate_idle()

#Class View
class View:
    def __init__(self, buffer, producers, consumers):
        self.buffer = buffer
        self.producers = producers
        self.consumers = consumers

    #function animate
    def animate(self):
        with Live(self.render(), screen = True, refresh_per_second = 10) as live:
            while True:
                live.update(self.render())

    #function render
    def render(self):
        match self.buffer:
            case PriorityQueue():
                title = "Priority Queue"
                products = map(str, reversed(list(self.buffer.queue)))
            
            case LifoQueue():
                title = "Stack"
                products = list(self.buffer.queue)

            case Queue():
                title = "Queue"
                products = reversed(list(self.buffer.queue))

            case _:
                title= products = ""
