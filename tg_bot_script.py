import os
import sqlite3

from telebot import types, TeleBot
from google.cloud import dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\dasha\small-talk-pwvh-41523ba9f162.json'

bot = TeleBot("7036415516:AAGxHelplPpo5SZB0N3dWMjg1YO366-UYJg")

users = {}


def connect_from_database(query):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def create_data_base():
    """Создаем таблицу для хранения информации"""

    # TODO: Дополнить модель хранения данных

    connect_from_database("CREATE TABLE IF NOT EXISTS users ("
                          "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "chat_id VARCHAR(256),"
                          "name VARCHAR(256),"
                          "surname VARCHAR(256),"
                          "job VARCHAR(256)"
                          ");")


def create_user(chat_id):
    connect_from_database(f"INSERT INTO users (chat_id, name, surname, job) "
                          f"VALUES ({chat_id}, "
                          f"'{users[chat_id]['name']}', "
                          f"'{users[chat_id]['surname']}', "
                          f"'{users[chat_id]['job']}');")


def get_markup_from_button():
    """Оформление для кнопочек"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_registration = types.KeyboardButton("Начать работу")
    markup.add(btn_registration)
    return markup


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "Хотите стать экспертом в IT? \n Добро пожаловать на нашу образовательную платформу CODE "
                     "BRAIN, где мы откроем перед вами мир системной аналитики, Java-разработки и "
                     "фронтенд-технологий!\n Наши курсы разработаны профессионалами индустрии, чтобы вы получили "
                     "только ценные знания и практические навыки. 🚀 \n С нами вы освоите каждый аспект создания "
                     "программного обеспечения - от бизнес-анализа и проектирования баз данных до "
                     "веб-интерфейсов и мобильных приложений.\n Присоединяйтесь к нашему сообществу студентов, "
                     "которые уже работают в крпуных компаниях!  Давайте вместе сделаем ваши IT-мечты "
                     "реальностью! 💻\n Для начала работы, нажми кнопку “Начать работу”".
                     format(message.from_user), reply_markup=get_markup_from_button())


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == "Начать работу":
        register(message)
    else:
        ai_text = little_ai_for_work(message=message.text)
        bot.send_message(message.chat.id, ai_text if ai_text else "Не понял тебя, напиши /help")


def register(message):
    bot.send_message(message.chat.id, "Давай знакомиться,\n Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text
    users[message.chat.id] = {"name": name}
    bot.send_message(message.chat.id,
                     f"Давай продолжим знакомство, {users[message.chat.id]['name']} \n Твоя фамилия?")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    surname = message.text
    users[message.chat.id]["surname"] = surname
    bot.send_message(message.chat.id, "Где ты работаешь/учишься?)")
    bot.register_next_step_handler(message, get_job)


def get_job(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Курс по системной аналитке", callback_data='analytics')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Курс Java - азработки", callback_data='java')
    btn3 = types.InlineKeyboardButton("Курс frontend - разработки", callback_data='front')
    markup.row(btn2, btn3)
    bot.reply_to(message,
                 "🌟 А теперь самое сложное, какой курс тебе интересен? 🤔💻\n 👉 Готов погрузиться в мир системной "
                 "аналитики и раскрыть потенциал бизнеса? Выбирай курс по системной аналитике!\n👉 Мечтаешь стать "
                 "профи в  Java и создавать высокоэффективные приложения? Добро пожаловать на курс по "
                 "Java-разработке! \n 👉 Или же вам по душе фронтенд и создание красивых и удобных пользовательских "
                 "интерфейсов? Не упустите возможность пройти курс по фронтенд разработке! \n Выбор за вами!  💪💡✨",
                 reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: analytics)
def callback_query(callback):
    callback.data = 'analytics'
    bot.send_message(message.chat.id,
                     "Добро пожаловать в захватывающий мир системной аналитики!\n На нашем курсе вы узнаете не "
                     "только про методы анализа бизнес-процессов, моделирования систем и принятия стратегически "
                     "важных решений, но и приобретете навыки, необходимые для эффективного взаимодействия с "
                     "бизнес-заказчиками, определения требований к ПО и управления проектами.\n Присоединяйтесь к "
                     "нам и станьте востребованным специалистом в области системной аналитики!\n Для регистрации "
                     "на курс, нажми кнопку “Далее”")
    bot.register_next_step_handler(message, get_register)


@bot.callback_query_handler(func=lambda callback: java)
def callback_query(callback):
    callback.data = 'java'
    bot.send_message(message.chat.id,
                     "Добро пожаловать в захватывающий мир Java-разработки! 🖥️ \nГотов освоить один из самых "
                     "популярных языков программирования и стать востребованным специалистом в IT-индустрии? \n "
                     "На нашем курсе по Java-разработке вы узнаете все от основных концепций до продвинутых "
                     "техник, который помогут вам создавать мощные, масштабируемые и надежные приложения. \n "
                     "Присоединяйтесь к сообществу энтузиастов! 🌟👨‍ \n \n Для регистрации на курс, нажми кнопку "
                     "“Далее”")
    bot.register_next_step_handler(message, get_register)


@bot.callback_query_handler(func=lambda callback: front)
def callback_query(callback):
    callback.data = 'front'
    bot.send_message(message.chat.id,
                     "Добро пожаловать в захватывающий мир фронтенд-разработки! \n С нашим курсом вы научитесь "
                     "создавать красивые, интерактивные и интуитивно понятные веб-интерфейсы. Мы получите не "
                     "только ключевые знания в области фронтенд разработки, но узнаете и про лучшие практики, "
                     "которые помогут вам стать профессионалом в данной сфере! \n Присоединяйтесь к нам и "
                     "превратите свою страсть к дизайну и программированию в профессиональное преимущество! \n \n "
                     "Для регистрации на курс, нажми кнопку “Далее”")
    bot.register_next_step_handler(message, get_register)


def get_register(message):
        markup = types.InlineKeyboardMarkup()
        btn4 = types.InlineKeyboardButton("Далее")
        bot.send_message(message,  "Есть ли у тебя базовые знания по данной дисциплине?")
        if message.text.lower() in ("да", "yes", "немного"): bot.send_message(message.chat.id,
                         "Тогда реши тестовое задание и получи скидку 20% на все обучение. Ссылка на тестовое задание "
                         "(гугл-док)",

        create_user(message.chat.id))
        else: bot.send_message(message.chat.id,
                         "Не расстраивайся! Дарим тебе скидку 15% на все обучение + 2 встречи с ведущими "
                         "преподавателями курсов!")


    ##bot.send_message(message.chat.id, ai_text if ai_text else "Погнали!")


def little_ai_for_work(project_id="small-talk-pwvh", session_id="test", message="", language_code="ru_RU"):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=message, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


create_data_base()
bot.polling(none_stop=True)
