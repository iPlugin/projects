#pip install aiogram==2.21

import configparser

from aiogram import Bot, Dispatcher, executor, types

import messages, stickers_emojis


config = configparser.ConfigParser()
config.read("settings.ini")

bot = Bot(config["TodoTamerBot"]["token_api"])
dp = Dispatcher(bot)


async def on_startup(_):
    print(messages.run_bot)

@dp.message_handler(commands=["start"])
async def command_start(msg: types.Message):
    await bot.send_sticker(msg.chat.id, sticker=stickers_emojis.stickers_1)
    await msg.answer(text=messages.command_start, parse_mode="HTML")
    await msg.delete()

@dp.message_handler(content_types=["sticker"])
async def get_stikers_id(msg: types.Message):
    await msg.reply(messages.get_sticker_id + msg.sticker.file_id, parse_mode="HTML")

@dp.message_handler(commands=["help"])
async def command_help(msg: types.Message):
    await bot.send_sticker(msg.from_user.id, sticker=stickers_emojis.stickers_2)
    await msg.answer(messages.command_help, parse_mode="HTML")
    await msg.delete()

@dp.message_handler()
async def command_NotFound(msg: types.Message):
    await bot.send_sticker(chat_id=msg.chat.id, sticker=stickers_emojis.stickers_3)
    await bot.send_message(chat_id=msg.chat.id, text=f"Нема такої команди \"{msg.text}\"")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)