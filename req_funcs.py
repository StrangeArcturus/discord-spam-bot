from typing import Union
from json import loads
from asyncio import sleep

import requests

class RequestSender:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.set_token('')
    
    def set_token(self, token: str) -> None:
        self.session.headers['authorization'] = token

    async def send_message(self, token: str, chat_id: Union[int, str], message: str) -> dict:
        self.set_token(token)
        json_data = {'content': str(message), 'tts': False}
        r = self.session.post(
            f'https://discord.com/api/v9/channels/{chat_id}/messages',
            json=json_data,
            verify=False
        )
        answer = {
            'message': message
        }
        if 'id' in loads(r.text):
            message_id = str(loads(r.text)['id'])
            answer['message_id'] = message_id
        return answer

    async def delete_message(self, chat_id: Union[int, str], message_id: Union[int, str],
    message: str, username: str, delay: float):
        await sleep(delay)
        r = self.session.delete(f'https://discord.com/api/v9/channels/{chat_id}/messages/{message_id}', verify=False)
        if r.status_code == 204:
            print(f'Сообщение с ID {message_id} и содержимым [{message}] от [{username}] успешно удалено')
