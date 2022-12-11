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