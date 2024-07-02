import telebot
from telebot import types

API_TOKEN = "YOUR_API_TOKEN"

bot = telebot.TeleBot(API_TOKEN)

# Основное меню
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(types.KeyboardButton('📜 Каталог'))
main_menu.add(types.KeyboardButton('🛒 Оформить заказ'))
main_menu.add(types.KeyboardButton('📞 Связаться с оператором'))
main_menu.add(types.KeyboardButton('❓ Помощь'))

# Меню каталога
catalog_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
catalog_menu.add(types.KeyboardButton('Кожаные сумки'))
catalog_menu.add(types.KeyboardButton('Кошельки'))
catalog_menu.add(types.KeyboardButton('Ремни'))
catalog_menu.add(types.KeyboardButton('Браслеты'))
catalog_menu.add(types.KeyboardButton('🔙 Назад'))

# Описание товаров
items = {
    'Кожаные сумки': '\n 1 - шоппер\n 2 - поясная',
    'Кошельки': '\n 1 - бифолд\n 2 - портмоне',
    'Ремни': '\n 1 - брючный\n 2 - для джинс',
    'Браслеты': '\n 1 - мужские\n 2 - женские'
}

# Флаги для отслеживания текущего состояния
is_ordering = False
is_contacting_operator = False


# Команда /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global is_ordering, is_contacting_operator
    is_ordering = False
    is_contacting_operator = False
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в интернет-магазин изделий из кожи ручной работы!\nЧем могу помочь?",
        reply_markup=main_menu
    )


# Обработка кнопки "📜 Каталог"
@bot.message_handler(func=lambda message: message.text == '📜 Каталог')
def show_catalog(message):
    global is_ordering, is_contacting_operator
    is_ordering = False
    is_contacting_operator = False
    bot.send_message(
        message.chat.id,
        "Вот наш каталог товаров. Выберите категорию:",
        reply_markup=catalog_menu
    )


# Обработка кнопок каталога
@bot.message_handler(func=lambda message: message.text in items.keys())
def show_item_description(message):
    global is_ordering, is_contacting_operator
    is_ordering = False
    is_contacting_operator = False
    item = message.text
    description = items[item]
    bot.send_message(
        message.chat.id,
        f'{item}\n\n{description}\n\nДля оформления заказа жмите "Назад" и "Оформить заказ"',
        reply_markup=catalog_menu
    )


# Обработка кнопки "🔙 Назад"
@bot.message_handler(func=lambda message: message.text == '🔙 Назад')
def go_back(message):
    global is_ordering, is_contacting_operator
    is_ordering = False
    is_contacting_operator = False
    bot.send_message(
        message.chat.id,
        "Вы вернулись в главное меню.",
        reply_markup=main_menu
    )


# Обработка кнопки "🛒 Оформить заказ"
@bot.message_handler(func=lambda message: message.text == '🛒 Оформить заказ')
def order_item(message):
    global is_ordering, is_contacting_operator
    is_ordering = True
    is_contacting_operator = False
    bot.send_message(
        message.chat.id,
        "Для оформления заказа напишите название товара, порядковый номер и количество.\nПример: Сумка 1 - 1 шт."
    )


# Обработка кнопки "📞 Связаться с оператором"
@bot.message_handler(func=lambda message: message.text == '📞 Связаться с оператором')
def contact_operator(message):
    global is_ordering, is_contacting_operator
    is_ordering = False
    is_contacting_operator = True
    bot.send_message(
        message.chat.id,
        "Наш оператор свяжется с вами в ближайшее время. Пожалуйста, оставьте свои контактные данные."
    )


# Обработка кнопки "❓ Помощь"
@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
def help_user(message):
    global is_ordering, is_contacting_operator
    is_ordering = False
    is_contacting_operator = False
    bot.send_message(
        message.chat.id,
        "Узнать более подробную информацию можно на сайте leatherworkshop.com",
        reply_markup=main_menu
    )


# Обработка сообщений в меню заказа и связи с оператором
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    global is_ordering, is_contacting_operator
    if is_ordering or is_contacting_operator:
        bot.send_message(
            message.chat.id,
            "Ваш запрос в обработке. Дождитесь ответа оператора для согласования заказа."
        )
    else:
        bot.send_message(
            message.chat.id,
            "Неизвестная команда. Пожалуйста, используйте кнопки меню."
        )


bot.polling()
