# -*- coding: utf-8 -*-
from typing import Optional

from discord.client import Client
from discord import ClientUser


class MyClient(Client):
    """
    Простая надстройка над имеющимся ботом,
    дабы можно было гибко придавать ему токен
    """
    user: ClientUser

    token: Optional[str] = None

    def set_token(self, token: str) -> None:
        self.token = token
