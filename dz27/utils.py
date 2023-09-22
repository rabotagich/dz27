import random
from aiogram import types

MATH_OPERATORS = ['+', '-', '*', '/']

def gen_example(min_max_num=(1,10), operators=MATH_OPERATORS):
    num1 = random.randint(*min_max_num)
    num2 = random.randint(*min_max_num)
    operator = random.choice(MATH_OPERATORS)
    example = f'{num1} {operator} {num2}'
    if operator == '/':
        while num1 % num2 != 0:
            num1 = random.randint(*min_max_num)
            num2 = random.randint(*min_max_num)
            example = f'{num1} {operator} {num2}'
    return example , int(eval(example))

def gen_unique_examples(count=4):
    examples = {}
    while len(examples) != count:
        example, answer = gen_example()
        if answer not in examples:
            examples[answer] = example
    return examples

def gen_keyboard(examples):
    keyboard = types.InlineKeyboardMarkup()
    for key, value in examples:
        keyboard.add(types.InlineKeyboardButton(text=key, callback_data=f'game_{value}'))
    return keyboard



if __name__ == '__main__':
    # print(gen_example())
    # print(gen_unique_examples())
    examples = list(gen_unique_examples().items())
    print(examples)
    true_example = random.choice(examples)
    print(true_example)
    for i, exaple in enumerate(examples):
        if exaple == true_example:
            examples[i] = (exaple[0], 'true')
        else:
            examples[i] = (exaple[0], 'false')
    print(examples)
    # keyboard = gen_keyboard(examples)