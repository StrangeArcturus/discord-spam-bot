# -*- coding: utf-8 -*-
from funcs import print_with_logging, check_key_on_pretty
from tg_bot import executor, dp
from bot import bot

# from dotenv import dotenv_values
from env import config
import multitasking
import psutil

from getpass import getpass
from os import mkdir, name
import traceback
import signal


def kill_me(self, cls):
    #process_name = "python main.py" if name == 'nt' else "python3 main.py"
    process_name = f"python{'' if name == 'nt' else '3'} {__file__}"
    try:
        print(f'Killing processes {process_name}')
        processes = psutil.process_iter()
        for process in processes:
            try:
                print(f'Process: {process}')
                print(f'id: {process.pid}')
                print(f'name: {process.name()}')
                print(f'cmdline: {process.cmdline()}')
                #if process_name == process.name() or process_name in process.cmdline():
                if process_name == ' '.join(process.cmdline()):
                    print(f'found {process.name()} | {process.cmdline()}')
                    process.terminate()
            except Exception:
                print(f"{traceback.format_exc()}")

    except Exception:
        print(f"{traceback.format_exc()}")
    finally:
        multitasking.killall(self, cls)
        exit()


signal.signal(signal.SIGINT, kill_me)
# config = dotenv_values('./.env')
log_path = config["LOGGING_FILE"]
my_bots_path = str(config["TEMPORARY_BOTS_NAMES"])
repled_msg_ids_path = str(config["TEMPORARY_MESSAGE_ID_PATH"])

for elem in my_bots_path.split('/')[:-1]:
    try: mkdir(elem)
    except: pass
with open(my_bots_path, 'w', encoding='utf-8') as file:
    file.write('')
"""
for elem in repled_msg_ids_path.split('/')[:-1]:
    try: mkdir(elem)
    except: pass
with open(repled_msg_ids_path, 'w', encoding='utf-8') as file:
    file.write('')
"""
multitasking.set_engine("process")
# настройки для обхода питоновского GIL и оптимального использования процессов и ядер
print_with_logging(
    "[multitasking] Using multiprocess-technology for bypassing python's GIL",
    log_path
)
with open(str(config['TOKENS']), 'r', encoding='utf-8') as file:
    bots_count = len(file.read().splitlines())
threads_count = multitasking.config["CPU_CORES"] * bots_count + 2
multitasking.set_max_threads(threads_count)
print_with_logging(
    f"[multitasking] Set maximal processes for python tasks. Count of them is {threads_count}",
    log_path
)


def main():
    with open(str(config['TOKENS']), 'r', encoding='utf-8') as file:
        tokens_list = file.read().splitlines()

    @multitasking.task
    def run_tg_bot_as_task() -> None:
        print_with_logging(
            '[telegram] Bot started success',
            log_path
        )
        executor.start_polling(dp, skip_updates=True)

    run_tg_bot_as_task()

    for token in tokens_list:
        @multitasking.task
        def run_ds_bot_as_task() -> None:
            bot.token = token
            print_with_logging(
                f"[multitasking] Will be started discord-userbot with token {token}",
                log_path
            )
            bot.run(token, bot=False)

        run_ds_bot_as_task()


if __name__ == "__main__":
    user_id = getpass("Your unique password\nВаш уникальный пароль: ")
    if not check_key_on_pretty(user_id):
        print("Your password is incorrect. Program finished.\nВаш пароль некорректен. Программа завершена.")
        exit()
    print("Password is correct. Next step./Пароль верный. Следующий шаг.")
    print()
    main()
