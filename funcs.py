# -*- coding: utf-8 -*-
from markovify import NewlineText
# from dotenv import dotenv_values
from env import config

from keygen import check_key_on_pretty

from typing import Optional
from datetime import datetime as dt


# config = dotenv_values('./.env')
log_path = config["LOGGING_FILE"]


def print_with_logging(log_string: str, path: Optional[str]) -> None:
    """
    Logging with choice of log to file
    """
    log_string = f"--{dt.now()}--\n{log_string}"
    if path:
        with open(path, 'a', encoding='utf-8') as file:
            print(log_string, file=file)
    else:
        print(log_string)


async def generate_new_words_from_text(text: str):
    """
    Generate sentence from words in `text`
    """
    text = text.lower().strip()
    size = 1
    text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000)# or choice(text.splitlines())
    while True:
        text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
        sentence = text_model.make_sentence(tries=1000)# or choice(text.splitlines())
        if sentence is not None:
            break
        else:
            size += 1
    print_with_logging(f'[markovify] Generated some new text: {sentence}', log_path)
    return sentence


async def exactly_float_parse(arg) -> float:
    """
    If `arg` not float-type, return `0.1`
    """
    answer: float = 0.1
    if not isinstance(arg, (int, float)):
        try:
            answer = float(arg)
        except:
            answer = 0.1
    return answer
