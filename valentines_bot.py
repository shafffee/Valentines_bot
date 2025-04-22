import telebot
from telebot import types
import pickle
from pathlib import Path
import logging
import time

token = '7440210952:AAFwA4ZDp1RWTynFF1aXQHBHZOZxKr2cEmQ'
first_options = ['🎩 Официальный', '😊 Дружеский','😂 Забавный']
second_options = ['🏢 О работе', '💊 Фармацевтика', '💡 Просто хорошее настроение']

first_question = "Какой стиль поздравления вам по душе? 😊 Давайте вместе создадим теплую и душевную открытку для ваших коллег."
second_question = "Какая тематика вам кажется наиболее подходящей? 🤔 Выберите из предложенных вариантов, чтобы ваше поздравление получилось идеальным!"
finish_message = "Сделано с любовью! 💕 Отправляйте эту особенную открыточку вашим коллегам, чтобы поднять им настроение!"
again_button = 'Еще одна валентинка не помешает! 😉'

savefile = Path(".\\data\\choises.dat")

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.INFO,
    filename=".\\data\\log.log",
    encoding="utf-8",
    filemode="a",
    format='{asctime}|\t{message}',
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)


loaded_images = {}

choises = {}
def save(choises):
    with open(savefile, 'wb+') as f:
        pickle.dump(choises, f)

if(savefile.exists()):
    with open(savefile, 'rb') as f:
        choises = pickle.load(f)

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
    for option in first_options:
        markup.add(types.KeyboardButton(option))
    bot.send_message(message.from_user.id, first_question, reply_markup=markup)
    choises[message.from_user.id]=""
    save(choises)
    logging.info("user "+str(message.from_user.id)+"\t added")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if not(message.from_user.id in choises):
        choises[message.from_user.id]=""
    if len(choises[message.from_user.id])==0:
        for o1 in range(len(first_options)):
            if message.text==first_options[o1]:
                choises[message.from_user.id]=str(o1)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
                for option in second_options:
                    markup.add(types.KeyboardButton(option))
                bot.send_message(message.from_user.id, second_question, reply_markup=markup)

                logging.info("user "+str(message.from_user.id)+"\t chose "+str(o1)+" on the first question")
                break;

    if len(choises[message.from_user.id])==1:
        for o2 in range(len(second_options)):
            if message.text==second_options[o2]:
                choises[message.from_user.id]+=str(o2)
                logging.info("user "+str(message.from_user.id)+"\t chose "+str(o2)+" on the second question")
                
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
                markup.add(types.KeyboardButton(again_button))
                
                bot.send_message(message.from_user.id, finish_message, reply_markup=markup)
                if not(choises[message.from_user.id] in loaded_images):
                    photo = open(".\\images\\"+choises[message.from_user.id]+".jpg",'rb')
                    loaded_images[choises[message.from_user.id]] = bot.send_photo(message.from_user.id,photo).photo[0].file_id
                else:
                    bot.send_photo(message.from_user.id,loaded_images[choises[message.from_user.id]])
                logging.info("user "+str(message.from_user.id)+"\t got image "+str(choises[message.from_user.id]))
                break;
    if len(choises[message.from_user.id])==2:
        if message.text==again_button:
            choises[message.from_user.id]=""
            logging.info("user "+str(message.from_user.id)+"\t restarted")
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
            for option in first_options:
                markup.add(types.KeyboardButton(option))
            bot.send_message(message.from_user.id, first_question, reply_markup=markup)

    save(choises)

if __name__ == '__main__':
  while True:
    try:
      bot.polling(none_stop=True, interval = 0)
    except:
      time.sleep(0.1)
