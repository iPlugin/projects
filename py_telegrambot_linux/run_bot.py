import asyncio
import logging
import sys
from os import getenv

import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold
from aiogram.utils import executor
from dotenv import dotenv_values
from script import get_hdd, get_ram, get_ram_metrics, get_hdd_metrics


# for email
import smtplib
import os
from email.mime.text import MIMEText


config = dotenv_values(".env")

# Bot token can be obtained via https://t.me/BotFather
TOKEN = config.get("BOT_TOKEN")
GROUP_ID = config.get("GROUP_ID")
EMAIL_LOGIN = config.get("EMAIL_LOGIN")
EMAIL_KEY = config.get("EMAIL_KEY")
MIN_RAM = 10
MIN_HDD = 10


bot = Bot(TOKEN, parse_mode="HTML")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher(bot)


def get_start_kb():
    """Функція отримання стартової клавіатури"""
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    check_btn = KeyboardButton('DISK RAM 💾')
    carfax_btn = KeyboardButton('DISK HDD 💿')
    help_btn = KeyboardButton('HELP ME')
    # cancel_btn = KeyboardButton('Скасувати операцію')
    start_kb.add(check_btn, carfax_btn).add(help_btn)  # , cancel_btn)
    return start_kb


@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=get_start_kb())


@dp.message_handler(text="DISK RAM 💾")
async def ram_handler(message: Message):
    metrics = get_ram_metrics()

    info = "RAM 💾 \n" \
           f"Загально: {metrics[0] / (1024 ** 3):.2f} GB\n" \
           f"Залишок: {metrics[1] / (1024 ** 3):.2f} GB\n" \
           f"Використано: {metrics[2] / (1024 ** 3):.2f} GB\n"
    await message.answer(info, reply_markup=get_start_kb())


@dp.message_handler(text="DISK HDD 💿")
async def hdd_handler(message: Message):
    metrics = get_hdd_metrics()

    info = "HDD 💾 \n" \
           f"Загально: {metrics[0] / (1024 ** 3):.2f} GB\n" \
           f"Залишок: {metrics[1] / (1024 ** 3):.2f} GB\n" \
           f"Використано: {metrics[2] / (1024 ** 3):.2f} GB\n"
    await message.answer(info, reply_markup=get_start_kb())


@dp.message_handler(text="HELP ME")
async def help_handler(message: Message):
    metrics = get_hdd_metrics()

    info = "Привіт\n" \
           f"Цей бот вимірює пам'ять дисків RAM і HDD\n" \
           f"Якщо виникли проблеми з ботом пиши @AndriyDutka\n"
    await message.answer(info, reply_markup=get_start_kb())


@dp.message_handler()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def check_ram():
    ram_persent = get_ram()
    hdd_persent = get_hdd()

    if ram_persent <= MIN_RAM:
        msg = f"| Warning | RAM disk | {ram_persent}% free space |"
        await bot.send_message(chat_id=GROUP_ID, text=msg)
        send_email(msg)
    
    if hdd_persent <= MIN_HDD:
        msg = f"| Warning | HDD disk | {hdd_persent}% free space |"
        await bot.send_message(chat_id=GROUP_ID, text=msg)
        send_email(msg)



async def scheduler():
    aioschedule.every(1).hours.do(check_ram)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())



# For email
def send_email(message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(EMAIL_LOGIN, EMAIL_KEY)
        msg = MIMEText(message)
        msg["Subject"] = "Click me please"
        server.sendmail(EMAIL_LOGIN, EMAIL_LOGIN, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    main()
