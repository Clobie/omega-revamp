# main.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from core.core import Core

core = Core(
    config_path = "./config/bot.conf"
)

async def main_thread():
    result = await core.run()
    if not result:
        print("[Main] Core run failed, exiting.")
        sys.exit(1)

asyncio.run(main_thread())