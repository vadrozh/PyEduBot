import logging
import telebot
from config import TOKEN
from telebot import types

# logging

logger = telebot.logger.setLevel(logging.DEBUG)

user_dict = {}

# bot
bot = telebot.TeleBot(TOKEN)


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


@bot.message_handler(commands=['start', 'help'])
def start_msg(message):
    # some info here
    msg = bot.reply_to(message, 'Hey! Let\'s begin our story! What\'s your name?')
    bot.register_next_step_handler(msg, name_step)


def name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Tell us your age.')
        bot.register_next_step_handler(msg, age_step)
    except Exception as e:
        bot.reply_to(message, 'Something went wrong...')


def age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, sex_step)

    except Exception as e:
        bot.reply_to(message, 'Something went wrong...')


def sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'Something went wrong...')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling()
