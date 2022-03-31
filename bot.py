# -*- coding: utf-8 -*-
from discord.channel import TextChannel
from discord import Message, ClientUser, MessageReference # тоже для типа

# from dotenv import dotenv_values # переменные среды
from env import config

import traceback
from re import fullmatch # для детекта ссылок в сообщениях по регулярке
from asyncio import sleep
from typing import Optional
from random import random, randint

from my_bot_class import MyClient
from req_funcs import RequestSender
from tg_bot import bot as tg_bot # сам бот из телеги
from funcs import generate_new_words_from_text, exactly_float_parse, print_with_logging


# инициализация всякой всячины
bot = MyClient()
# config = dotenv_values('./.env')
delay = int(config["DELETING_DELAY"])
typing_delay = int(config["TYPING_MESSAGE_TIME"])
log_path = config["LOGGING_FILE"]
is_deleting = str(config["IS_DELETING"])
my_bots_path = str(config["TEMPORARY_BOTS_NAMES"])
msg_ids = str(config["TEMPORARY_MESSAGE_ID_PATH"])
chats_ids = str(config["CHATS"])
sender = RequestSender()


@bot.event
async def on_ready() -> None:
    bot_info = f"{bot.user.name}#{bot.user.discriminator}"
    print_with_logging(f'[discord] Bot {bot_info} started successs with token {bot.token}', log_path)
    with open(my_bots_path, 'a', encoding='utf-8') as file:
        file.write(f"{bot_info}\n")


@bot.event
async def on_message(message: Message) -> None:
    try:
        chance = float(str(config["ANSWER_CHANCE"]))
        # параметры выносим для удобства, подсказок по типам и просто чтобы не дёргать свойства в рантайме
        channel: TextChannel = message.channel
        user: ClientUser = bot.user # анализатору не нравится, что свойство юзера может быть None, это единственный триггер
        slowmode_delay = channel.slowmode_delay if hasattr(channel, 'slowmode_delay') else 0

        print_with_logging(
            f"[discord] Bot see new message in channel {channel.name} {channel.id}",
            log_path
        )

        if message.author == bot.user: return # если сообщение моё -- завершить функцию

        with open(chats_ids, 'r', encoding='utf-8') as file:
            chats_list = file.read().splitlines()
        
        if str(channel.id) not in chats_list: return # если айди чата отсутствует в файле с ними -- завершить

        with open(my_bots_path, 'r', encoding='utf-8') as file:
            my_bots = file.read().splitlines()
        if f"{message.author.name}#{message.author.discriminator}" in my_bots:...
            #chance *= randint(2, 5) # рандомизация увеличения шанса

        if random() * randint(2, 5) > chance: return # вероятность ответа или не ответа
        await sleep(
            randint(slowmode_delay, slowmode_delay + 10)
        ) # ожидание, если включен медленный режим
        # юзаем "<юзернейм> набирает сообщение/печатает для правдоподобности"
        async with channel.typing():
            # answer = await channel.history().flatten() # как варик
            """
            answer = [
                msg.content async for msg in channel.history(limit=1_000_000) if msg.author != bot.user
            ]
            """
            # задействовал бы списковое включение, так как оно более быстрое
            # но циклом будет и понятнее, и удобнее, и читебельнее
            # и всё за один проход выполню
            await sleep(await exactly_float_parse(typing_delay) or 0) # имитация набора текста
            answer = []
            counter = 0 # хз зачем, но в доках есть счётчик
            # ids = [] # хз зачем тут это
            # бежим по истории сообщений (всю историю взять невозможно,
            # поэтому бежим по невообразимо большому кол-ву сообщений, по ляму)
            async for msg in channel.history(limit=1_000_000):
                if msg.author != user:
                    delete_this_msg = False
                    current_id = msg.id
                    # <-- check replies
                    if hasattr(msg, 'reference'):
                        reference: Optional[MessageReference] = msg.reference
                        delete_this_msg = True # включить флаг, если есть варнинг
                        with open(msg_ids, 'r', encoding='utf-8') as file:
                            ids = file.read().splitlines()
                        if str(msg.id) in ids:
                            return
                        try:
                            if (reference and reference.resolved and
                                str(user.id) == str(reference.resolved.author.id)): # and current_id not in ids:
                                reply_content = msg.content
                                print_with_logging(
                                    f'[discord][{user.name}] Ваше сообщение переслали в ChatID: {channel.id}',
                                    log_path
                                )
                                # ids.append(current_id)

                                bot_msg_resp = str(await tg_bot.send_message(
                                    str(config["MY_TG_ID"]), (
                                    f'Ваше сообещние переслали\n'
                                    f'\tChatID:\n\t\t{channel.id}\n'
                                    f'\tChatName:\n\t\t{channel.name}\n'
                                    f'\tChatGuld:\n\t\t{channel.guild.name}\n'
                                    f'\tUsername:\n\t\t{user.name}\n'
                                    f'\tToken:\n\t\t{bot.token}\n'
                                    f'\tMsg id:\n\t\t{current_id}\n'
                                    f'\tMsg text:\n\t\t{reply_content}'
                                )))
                                if 'from_user' in bot_msg_resp:
                                    print_with_logging(
                                        f'[discord] -> [telegram] Сообщение в Telegram успешно отправлено',
                                        log_path
                                    )
                                else:
                                    print_with_logging(
                                        f'[discord] -> [telegram] Ошибка при отправке сообщения в Telegram: {bot_msg_resp}',
                                        log_path
                                    )
                                with open(msg_ids, 'a', encoding='utf-8') as file:
                                    file.write(f'{msg.id}\n')
                        except Exception as e:
                            #print(f"{traceback.format_exc()}")
                            print(f'Exception {e.__class__.__name__} occured at user... with text {str(e)}')
                            #await tg_bot.send_message("567226650", f"Exception {e.__class__.__name__} occured at user... with text {str(e)}")

                    # --> check replies

                    # <-- check tags
                    current_message = msg.content.replace('\n', '').replace('\r', '')
                    if (f'<@!{str(user.id)}>' in current_message or
                        f"{user.name}#{user.discriminator}" in current_message or
                        f"@{user.name}" in current_message or
                        f"@{user.id}" in current_message): # and current_id not in ids:

                        delete_this_msg = True # включить флаг, если есть варнинг
                        with open(msg_ids, 'r', encoding='utf-8') as file:
                            ids = file.read().splitlines()
                        if str(msg.id) in ids:
                            return
                        print_with_logging(
                            f'[discord][{user.name}] Вас упомянули в ChatID: {channel.id}',
                            log_path
                        )
                        # ids.append(current_id) if current_id not in ids else ...
                        bot_msg_resp = str(await tg_bot.send_message(
                            str(config["MY_TG_ID"]), (
                            f'Вас упомянули\n'
                            f'\tChatID:\n\t\t{channel.id}\n'
                            f'\tChatName:\n\t\t{channel.name}\n'
                            f'\tChatGuld:\n\t\t{channel.guild.name}\n'
                            f'\tUsername:\n\t\t{user.name}\n'
                            f'\tToken:\n\t\t{bot.token}\n'
                            f'\tMsg id:\n\t\t{current_id}\n'
                            f'\tMsg text:\n\t\t{current_message}'
                        )))
                        if 'from_user' in bot_msg_resp:
                            print_with_logging(
                                f'[discord] -> [telegram] Сообщение в Telegram успешно отправлено',
                                log_path
                            )
                        else:
                            print_with_logging(
                                f'[discord] -> [telegram] Ошибка при отправке сообщения в Telegram: {bot_msg_resp}',
                                log_path
                            )
                        with open(msg_ids, 'a', encoding='utf-8') as file:
                                    file.write(f'{msg.id}\n')
                    answer.append(msg.content)
                    await msg.delete(delay=0) if delete_this_msg else ...
                    # удаление сообщения с варнингом за ненадобностью
                    # --> check tags
                else:
                    if is_deleting == 'yes':
                        # delay as in config in `.env` or momentally
                        await msg.delete(delay=(await exactly_float_parse(delay) or 0))
                        print_with_logging((
                            f'[discord] Deleted message in history with\n'
                            f'\tid:\n\t\t{msg.id}\n'
                            f'\tcontent:\n\t\t{msg.content}\n'
                            f'\tchannel:\n\t\t{channel.name}'
                            ),log_path
                        )
                counter += 1
            answer = list(filter(
                lambda msg: not fullmatch(r"^(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*$", msg),
                answer # проверка на ссылку
            )) # фильтр на сообщения с ссылками

            sentence = await generate_new_words_from_text('\n'.join(answer))
            print_with_logging(
                f"[discord] My answer into {channel.name}:\n{sentence}",
                log_path
            )
            #my_last_message = await channel.send(sentence)
            sender.set_token(bot.token)
            my_last_message = await sender.send_message(bot.token, channel.id, sentence)
            if is_deleting == 'yes':
                # delay в `.env` или моментально
                await sender.delete_message(
                    channel.id, my_last_message.get("message_id", "1"),
                    my_last_message["message"], bot.user.name , delay=(await exactly_float_parse(delay) or 0))
                print_with_logging(
                    f'[discord] Deleted message from channel {channel.name} with id: {message.id}',
                    log_path
                )
    except Exception as e:
        #print(f"{traceback.format_exc()}")
        print(f'Exception {e.__class__.__name__} occured at user... with text {str(e)}')
        #await tg_bot.send_message("567226650", f"Exception {e.__class__.__name__} occured at user... with text {str(e)}")
