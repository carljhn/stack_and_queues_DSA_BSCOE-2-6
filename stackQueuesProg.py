# Now suppose you’ve written a program with more than one flow of execution. Beyond being a valuable algorithmic tool, queues can help 
# abstract away concurrent access to a shared resource in a multithreaded environment without the need for explicit locking. 
# Python provides a few synchronized queue types that you can safely use on multiple threads to facilitate communication between them.

# In this section, you’re going to implement the classic multi-producer, multi-consumer problem using Python’s thread-safe queues. 
# More specifically, you’ll create a command-line script that lets you decide on the number of producers and consumers, their relative
# speed rates, and the type of queue:

import argparse
import threading
from dataclasses import dataclasses, field 
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
