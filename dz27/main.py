from random import randint, choice
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types

import logging
from utils import *

API_TOKEN ='6569387811:AAECcUzgYtZ1ixCbrI4feq8hqNQR5SaCw60'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

record = 0
score = 0
lose = 0
win = 0

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привіт")

@dp.message_handler(commands=['game'])
async def gen(message: types.Message):
    examples = list(gen_unique_examples().items())
    true_example = choice(examples)
    for i, exaple in enumerate(examples):
        if exaple == true_example:
            examples[i] = (exaple[0], 'true')
        else:
            examples[i] = (exaple[0], 'false')
    keyboard = gen_keyboard(examples)
    text = f"Обери правильну відповідь на приклад: {true_example[1]}"
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query_handler(text_contains='game_')
async def game(call: types.CallbackQuery):
    global score, lose, win, record
    
    answer = call.data.split('_')[1]
    if answer == 'true':
        await call.answer('Вірно')
        score += 1
        win += 1
    else:
        await call.answer('Невірно')
        score -= 1
        lose += 1
    if lose == 5:
        await call.message.answer(f'Ви програли. Ваш рахунок: {score}')
        score = 0
        lose = 0
        win = 0
        return
    if record < score:
        record = score


    examples = list(gen_unique_examples().items())
    true_example = choice(examples)
    for i, exaple in enumerate(examples):
        if exaple == true_example:
            examples[i] = (exaple[0], 'true')
        else:
            examples[i] = (exaple[0], 'false')
    keyboard = gen_keyboard(examples)
    text = f"----Ваш рахунок----\nРекорд:{record}\nВірно: {win}\nНевірно: {lose}\nРахунок: {score}\n\nОбери правильну відповідь на приклад: {true_example[1]}"
    await call.message.answer(text, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)