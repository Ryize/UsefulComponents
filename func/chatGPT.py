import random
import threading
import time

import openai
import os


def analyze_file(file_path):
    file_size = os.path.getsize(file_path)
    if file_size > 2048:
        with open(file_path, "r", encoding='utf-8') as file:
            chunks = [file.read(2048) for _ in range(file_size // 2048 + 1)]
        for chunk in chunks:
            chatGPT = ChatGPT()
            chatGPT.thread_send(chunk)
    else:
        with open(file_path, "r", encoding='utf-8') as file:
            code = file.read()
            chatGPT = ChatGPT()
            chatGPT.thread_send(code)


class ChatGPT:
    __api_keys = ()

    def __init__(self):
        openai.api_key = random.choice(self.__api_keys)
        self.model_engine = "text-davinci-003"

    def thread_send(self, *args, **kwargs):
        threading.Thread(target=self.print_result, args=args, kwargs=kwargs).start()
        time.sleep(1)

    def print_result(self, data, *args, **kwargs):
        if data:
            print(f'\n\n', '-' * 50, f'\nФрагмент кода: \n{data}\n Результат проверки:\n', self.send(
                f'Проанализируй код, найди в нём синтаксические ошибки и баги. Оцени сам код от 1 до 10:\n{data}\nПиши на русском языке.',
                *args, **kwargs).lstrip())

    def send(self, data) -> str:
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=data,
            max_tokens=2048,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return completion.choices[0].text
