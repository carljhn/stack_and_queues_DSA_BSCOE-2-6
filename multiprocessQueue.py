# Using multiprocessing.Queue for Interprocess Communication (IPC)

#Import libraries
import argparse
import multiprocessing
import queue
import time
from dataclasses import dataclass
from hashlib import md5
from string import ascii_lowercase