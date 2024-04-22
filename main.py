import telebot
from telebot import types
import sqlite3 

Token = '7036415516:AAGxHelplPpo5SZB0N3dWMjg1YO366-UYJg'
bot = telebot.TeleBot(Token)
name = ""
surname = ""
job = ""

# для старта работы, необходимо написать в чат /start


@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Зарегистрироваться")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Привет, друг! Добро пожаловать в мир аналитики 📊 \n Нажми кнопку зарегистрироваться".
                     format(message.from_user), reply_markup=markup)
    conn = sqlite3.connect('code.brain.sql')
    cur = conn.cursor()


    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(70), pass varchar('
                '70)')
    conn.commit()
    cur.close()
    conn.close

    bot.register_message_handler(message, register)
@bot.message_handler(content_types=['text'])
def register(message):
    if message.text == "Зарегистрироваться":
        bot.send_message(message.from_user.id, "Давай знакомиться,\n Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = message.text
    if message.text != "Зарегистрироваться":
        bot.send_message(message.from_user.id, "Давай продолжим знакомство," + name + "\n""Твоя фамилия?")
        bot.register_next_step_handler(message, get_surname)
    else:
        bot.send_message(message.from_user.id, "Не понял тебя, напиши /help")



def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Где ты работаешь/учишься?)")
    bot.register_next_step_handler(message, get_job)


def get_job(message):
    global job
    job = message.text
    bot.send_message(message.from_user.id,
                     "Тогда предлагаем тебе присоединиться к бесплатному курсу для тех, кто хочет изменить свою карьеру и жизнь!😊\n Освойте одну из самых востребованных профессий в IT и получите опыт для работы на коммерческих проектах \n Старт курса: 25 марта 2024 года \n Длительность: 2,5 месяца + защита \n Стоимость: 4500руб" " \n Готов присоединиться?")
    bot.register_next_step_handler(message, website)


def website(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Code Brain", url='https://job.promo-z.ru/analytic')
    markup.row (btn1)
    btn2 = types.InlineKeyboardButton("Пройти тестирование", callback_data='test')
    btn3 = types.InlineKeyboardButton("Пообщаться с менеджером", callback_data='cal')
    markup.row (btn2, btn3)
    bot.send_message(message.chat.id,
                     "Скорее, {0.first_name}! Осталось 10 свободных мест!)".
                     format(message.from_user), reply_markup=markup)


def get_course(message):
    global course
    course = message.text
    bot.send_message(message.from_user.id, "")
    bot.register_next_step_handler(message)

##@bot.callback_query_handler(func=lambda callback: True)
##def callback_message(callback):
  ##  if callback.data == "delete":
##bot.polling(none_stop=True, interval=0)
