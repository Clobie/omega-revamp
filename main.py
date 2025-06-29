# main.py

import os
import sys
import argparse
import asyncio

# Adjust sys.path for imports if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.core import Core
from utils.personality import PersonalityManager

def parse_args():
	parser = argparse.ArgumentParser(description="Discord Bot Launcher")
	parser.add_argument(
		"--config",
		type=str,
		default="./config/config.yaml",
		help="Path to bot configuration YAML file"
	)
	parser.add_argument(
		"--personalities",
		type=str,
		default="./config/personalities.yaml",
		help="Path to personalities YAML file"
	)
	return parser.parse_args()

async def main_thread():
	args = parse_args()

	core = Core(config_path=args.config)

	# Run core
	success = await core.run()
	if not success:
		print("[Main] Core run failed, exiting.")
		sys.exit(1)

if __name__ == "__main__":
	asyncio.run(main_thread())
