# In this section, you’ll write a rudimentary web crawler, which recursively follows links on a 
# specified website up to a given depth level and counts the number of visits per link. To fetch
# data asynchronously, you’ll use the popular aiohttp library, and to parse HTML hyperlinks, 
# you’ll rely on beautifulsoup4. 

#import libraries
import argparse
import asyncio
import sys
from collections import Counter
from typing import NamedTuple
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

#Class Job
class Job(NamedTuple):
    url: str
    depth: int = 1

    #function __lt__
    def __lt__(self, other):
        if isinstance(other, Job):
            return len(self.url) < len(other.url)

#Async function
async def main(args):
    session = aiohttp.ClientSession()
    try:
        links = Counter()
        queue = asyncio.Queue()
        # queue = asyncio.LifoQueue()
        # queue = asyncio.PriorityQueue()
        task = [
            asyncio.create_task(
                worker(
                    f"Worker-{i + 1}",
                    session, 
                    queue, 
                    links, 
                    args.max_depth,
                )
            )
            for i in range(args.num_workers)
        ]

        await queue.put(Job(args.url))
        await queue.join()

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        display(links)
    finally:
        await session.close()