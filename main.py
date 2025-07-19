# main.py

import os
import sys
import argparse
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.core import Core

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
	parser.add_argument(
		"--cogpath",
		type=str,
		default="./cogs",
		help="Path to the cogs directory"
	)
	parser.add_argument(
		"--cogconfig",
		type=str,
		default="./config/cogs.yaml",
		help="Path to the cogs configuration YAML file"
	)
	return parser.parse_args()

async def main_thread():
	args = parse_args()
	core = Core(
		config_path=args.config, 
		personalities_path=args.personalities, 
		cogs_path=args.cogpath, 
		cogs_config_path=args.cogconfig
	)
	success = await core.run()
	if not success:
		print("[Main] Core run failed, exiting.")
		sys.exit(1)

if __name__ == "__main__":
	try:
		asyncio.run(main_thread())
	except (KeyboardInterrupt, asyncio.CancelledError):
		print("\n[Main] Shutdown requested, exiting gracefully.")
		sys.exit(0)

