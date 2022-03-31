from dotenv import dotenv_values

import config_vars


try:
    config = dotenv_values('./env.env')
except:
    config = {
        i: key for i, key in vars(config_vars).items() if '__' not in i
    }
    """
    config = {
        "TOKENS": "TOKENS.txt",
        "CHATS": "CHATS_ID.txt",
        "TG_TOKEN": "5230920721:AAGc7FhnWNwHelIcTOo-T0ffriV8LW14A2s",
        "MY_TG_ID": "567226650",
        "TYPING_MESSAGE_TIME": 10,
        "IS_DELETING": "no",
        "DELETING_DELAY": 10,
        "ANSWER_CHANCE": 0.7,
        "LOGGING_FILE": "",
        "TEMPORARY_BOTS_NAMES": "./tmp/bots_names.txt",
        "TEMPORARY_MESSAGE_ID_PATH": "./tmp/message_ids.txt"
    }
    """
