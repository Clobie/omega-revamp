# main.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from core.omega import Omega

omega = Omega()

async def main_thread():
    await omega.run()

asyncio.run(main_thread())