import configparser
from random import randint


from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import messages, stickers_emojis

# config
config = configparser.ConfigParser()
config.read("settings.ini")

bot = Bot(config["TodoTamerBot"]["token_api"])
dp = Dispatcher(bot)



kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton("/help")
button_2 = KeyboardButton("/description")
button_3 = KeyboardButton("/❤️")
button_4 = KeyboardButton("/sendfoto")
button_5 = KeyboardButton("/location")
kb.add(button_1).add(button_2).add(button_3).add(button_4).insert(button_5)

async def on_startup(_):
    print(messages.run_bot)

@dp.message_handler(commands=["start"])
async def command_start(msg: types.Message):
    await bot.send_sticker(msg.chat.id, sticker=stickers_emojis.stickers_1)
    await msg.answer(text=messages.command_start, parse_mode="HTML", reply_markup=kb)
    await msg.delete()

@dp.message_handler(commands=["help"])
async def command_help(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id, text=messages.command_help, parse_mode="HTML")
    
@dp.message_handler(commands=["description"])
async def command_description(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id, text=messages.command_description)
    
@dp.message_handler(commands=["❤️"])
async def command_heard(msg: types.Message):
    await bot.send_sticker(chat_id=msg.chat.id, sticker=stickers_emojis.stickers_4)
    
@dp.message_handler(commands=["sendfoto"])
async def command_sendfoto(msg: types.Message):
    await bot.send_photo(chat_id=msg.chat.id, photo=stickers_emojis.foto_1)
    
@dp.message_handler(commands=["location"])
async def command_location(msg: types.Message):
    await bot.send_location(chat_id=msg.chat.id, latitude=randint(1, 100), longitude=randint(1, 100))
    
@dp.message_handler(content_types=["sticker"])
async def get_stikers_id(msg: types.Message):
    await msg.reply(messages.get_sticker_id + msg.sticker.file_id, parse_mode="HTML")
    
@dp.message_handler()
async def command_NotFound(msg: types.Message):
    await bot.send_sticker(chat_id=msg.chat.id, sticker=stickers_emojis.stickers_3)
    await bot.send_message(chat_id=msg.chat.id, text=f"Нема такої команди \"{msg.text}\"")





if __name__ == "__main__":
    
    executor.start_polling(dp, on_startup=on_startup)