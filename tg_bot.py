from aiogram import Bot, Dispatcher, executor
# from dotenv import dotenv_values
from env import config


# params = dotenv_values('./.env')
bot = Bot(str(config["TG_TOKEN"]))
dp = Dispatcher(bot)
