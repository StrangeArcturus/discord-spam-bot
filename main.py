from env import config
from main_ui import start_gui
from console import main, kill_me

import multitasking

import signal


multitasking.set_engine("process")
with open(str(config['TOKENS']), 'r', encoding='utf-8') as file:
    bots_count = len(file.read().splitlines())
threads_count = multitasking.config["CPU_CORES"] * bots_count + 2
multitasking.set_max_threads(threads_count)
signal.signal(signal.SIGINT, kill_me)


if __name__ == "__main__":
    start_gui(main)
