#!/usr/bin/env python3
"""Module for concurrent coroutines"""

import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:

    """Spawns wait_random n times and returns the delays in ascending order"""
    tasks = []

    for _ in range(n):
        tasks.append(wait_random(max_delay))

    delays = []

    for task in asyncio.as_completed(tasks):
        result = await task
        delays.append(result)

    return delays
