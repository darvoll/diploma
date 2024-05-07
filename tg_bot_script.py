import os
import sqlite3

from telebot import types, TeleBot
from google.cloud import dialogflow

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\dasha\PycharmProjects\diploma\small-talk-pwvh-41523ba9f162.json'

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
    btn_registration = types.KeyboardButton("Далее⬇️")
    btn_lend = types.KeyboardButton("Узнать подробнее")
    markup.add(btn_registration, btn_lend)
    return markup


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "Давай знакомиться! Code Brain - это образовательная платформа для начинающих специалистов и "
                     "тех, кто решил впервые попробовать свои силы IT 🤯 ".
                     format(message.from_user), reply_markup=get_markup_from_button())


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == "Далее⬇️":
        choice(message)
    else:
        ai_text = little_ai_for_work(message=message.text)
        bot.send_message(message.chat.id, ai_text if ai_text else "Не понял тебя, напиши /help")


def choice(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Системная аналитика", callback_data='analytics')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Java - разработка", callback_data='java')
    btn3 = types.InlineKeyboardButton("Frontend - разработка", callback_data='front')
    markup.row(btn2, btn3)
    bot.reply_to(message,
                 "Мы предоставляем обучение по трем направлениям: \n 🔹 Системная аналитика \n 🔹 Java-разработка для "
                 "начинающих \n 🔹 Основы Frontend-разработки \n Что интересует тебя больше всего?🔥",
                 reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: analytics)
def callback_query(callback):
    callback.data = 'analytics'
    bot.send_message(message.chat.id,
                     "Добро пожаловать в захватывающий мир системной аналитики!📚 \n На нашем курсе вы не только "
                     "пройдете теоретическую базу, узнаете  про методы анализа бизнес-процессов и многое другое, "
                     "но также попрактикуетесь в создании собственного проекта, который смело можете оставить в своем "
                     "портфолио 😎  \n 🔹 Старт курса: 10 июля 2024 года \n 🔹 Продолжительность: 2.5 месяца \n Формат "
                     "занятий: онлайн \n 🔹 Количество мест: 20 \n 🔹 Что нужно для обучения:  ноутбук/ компьтер \n 🔹"
                     "Стоимость курса: 7.999! 🔥")
    markup = types.InlineKeyboardMarkup()
    btn4 = types.InlineKeyboardButton("Купить курс", callback_data='buy')
    btn5 = types.InlineKeyboardButton("", callback_data='programm1')
    markup.row(btn4, btn5)
    callback.message.edit_reply_markup(btn4, btn5)


@bot.callback_query_handler(func=lambda callback: java)
def callback_query(callback):
    callback.data = 'java'
    bot.send_message(message.chat.id,
                     "Добро пожаловать в мир тайн и секретов Java-разработки! 👀 \n Это курс для тех, кто давно "
                     "мечтал попробовать себя в роли разработчика! С нами вы узнаете все от основных концепций до "
                     "продвинутых техник, который помогут вам создавать мощные, масштабируемые и надежные "
                     "приложения.🔹 \n Старт курса: 10 июля 2024 года 🔹\n Продолжительность: 2.5 месяца 🔹\n Формат "
                     "занятий: онлайн 🔹\n Количество мест: 20 🔹\n Что нужно для обучения: ноутбук/ компьтер 🔹\n "
                     "Стоимость курса: 8.999! 🔥")
    markup = types.InlineKeyboardMarkup()
    btn4 = types.InlineKeyboardButton("Купить курс", callback_data='buy')
    btn5 = types.InlineKeyboardButton("", callback_data='programm2')
    markup.row(btn4, btn5)
    callback.message.edit_reply_markup(btn4, btn5)


@bot.callback_query_handler(func=lambda callback: front)
def callback_query(callback):
    callback.data = 'front'
    bot.send_message(message.chat.id,
                     "Добро пожаловать в мир фронтенд-разработки! ☀️ \n С нашим курсом вы научитесь создавать "
                     "красивые, интерактивные и интуитивно понятные веб-интерфейсы! Вы получите не только ключевые "
                     "знания в области фронтенд разработки, но узнаете и про лучшие практики, которые помогут вам "
                     "стать профессионалом в данной сфере!🔹 \n Старт курса: 10 июля 2024 года 🔹\n "
                     "Продолжительность: 2.5 месяца 🔹\n Формат занятий: онлайн 🔹\n Количество мест: 20 🔹\n Что "
                     "нужно для обучения: ноутбук/ компьтер 🔹\n Стоимость курса: 8.999! 🔥")
    markup = types.InlineKeyboardMarkup()
    btn4 = types.InlineKeyboardButton("Купить курс", callback_data='buy')
    btn5 = types.InlineKeyboardButton("", callback_data='programm3')
    markup.row(btn4, btn5)
    callback.message.edit_reply_markup(btn4, btn5)


@bot.callback_query_handler(func=lambda callback: program1)
def callback_query(callback):
    callback.data = 'program1'
    bot.send_message(message.chat.id,
                     "📌Профессия “Системный аналитик” Введение. Команда разработки ПО.Жизненный цикл ПО. Методологии "
                     "разработки \n 📌Разработка требований \n Требования. Бизнес-требования \n Моделирование "
                     "бизнес-процессов \n Пользовательские и функциональные требования \n Нефункциональные требования "
                     "\n 📌Архтикектура \n API \n Авторизация \n Модель данных, ER-диаграмма \n  Базы данных \n  "
                     "Архитектура микросервисов и монолитов \n  Очереди сообщений \n Диаграмма последовательности \n "
                     "Проектирование UI \n Передача задач в разработку и тестирование \n Вопросы собеседования на "
                     "позицию системного аналитика ")


@bot.callback_query_handler(func=lambda callback: program2)
def callback_query(callback):
    callback.data = 'program2'
    bot.send_message(message.chat.id,
                     "📌Java Core 1. Вводное занятие. Знакомство. Обзор курса. Подготовка среды разработки. "
                     "Maven/Gradle. Первая программа ""Hello world"". \n 2. Простые типы данных, операции ними. "
                     "Условия, циклы, switch/case. Логические операции. \n 3. Введение в ООП. Классы, объекты, "
                     "конструкторы. Инкапсуляция, модификаторы доступа. Функции. Рекурсия. Область видимости "
                     "переменных.\n 4. Продвинутое ООП. Наследование, полиморфизм. Интерфейсы абстракция.  \n 5. "
                     "Обобщения. Коллекции: List, Мар, Set. Основные реализации коллекцій. Классы String, Integer, "
                     "Long, Double. \n 6. Многопоточность. Создание потоков. Управление потоками. Проблемы при работе "
                     "потоками. Синхронизация потоков. Happens Before. \n 7. Многопоточность. ExecutorService. Future и"
                     "CompletableFuture. ThreadLocal переменные. переменные. Atomic \n 8. Взаимодействие с БД. "
                     "JDBC.  \n 📌 Веб-разработка. Spring. Базы данных  \n 1. Введение Spring. Bean. Инициализация "
                     "бинов."
                     "Контекст Spring.  \n 2. Spring Boot. Архитектура. \n3. Конфигурация. Внедрение зависимостей. "
                     "@Qualifier, @Autoiwired  \n 4. Сервлеты. Spring MVC. Контроллеры. Жизненный цикл бинов.  \n 5. "
                     "Доступ к"
                     "данным. JPA. Понятие сущности, объектно-реляционное отображение. Связи между сущностями. \n 6. "
                     "Менеджер сущностей. Hibernate. Сервис-слой.  \n 7. Транзакции. Уровні изоляций.  \n 8. Spring "
                     "REST."
                     "CRUD операции. Репозитории. ExceptionHandler'ы. Entity Graph.  \n 9. Spring Security. "
                     "Авторизация."
                     "Доступ к ресурсам. FilterChain.  \n 10. Аспектно-ориентированное программирование. Spring AOP.  "
                     "\n 11."
                     "База данных. SQL. Join запросы. Индексы.")


@bot.callback_query_handler(func=lambda callback: program3)
def callback_query(callback):
    callback.data = 'program3'
    bot.send_message(message.chat.id,
                     "📌Программа курса \n 1.WEB - что, зачем и как \n 2. TypeScript \n 3. Обзор фреймворков и "
                     "трендов \n 4. React - не первый, но первый \n 5. Хранение данных во фронтенд фреймворках \n 6. "
                     "Стилизация, пре- и пост-процессоры, css фреймворки \n 7. Инфраструктура разработки \n 8. "
                     "Тестирование фронтенда \n 9. Оптимизация ")


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
