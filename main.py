import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import user_regis
import test
from chat_historiy import ChatAnalytics
import test  # предполагается, что у тебя есть модуль test
import telebot
import chat_historiy
import os
import bds

admin = [1978497895]


bot = telebot.TeleBot("7788275263:AAFspNCfZ0Bl3z_Kabc_f19HvISozRHNj-c")
user_chat_bas = 0

users_data = {}



def tekser(message):
    if message.text == '❇️ Начат чат ❇️':
        return True
    elif message.text == 'тех поддершка ☎️':
        return True
    elif message.text == "👥о себе👥":
        return True
    elif message.text == 'Назад':
        return True
    else:
        return False

def start_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bt = KeyboardButton("Отправить номер 📞", request_contact=True)
    markup.add(bt)
    return markup

def aliw():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    bt = KeyboardButton("❇️ Начат чат ❇️")
    bt1 = KeyboardButton("тех поддершка ☎️")
    bt2 = KeyboardButton("👥о себе👥")
    markup.add(bt,bt1,bt2)
    return markup

def admin_bt():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    bt = KeyboardButton("Анализ 24ч")
    bt1 = KeyboardButton("Анализ недели")
    bt2 = KeyboardButton("Анализ месяца")
    bt3 = KeyboardButton("Анализ года")
    bt4 = KeyboardButton("Полный Анализ Запрасов")
    bt5 = KeyboardButton("Анализ по Категориям")
    markup.add(bt,bt1,bt2,bt3,bt4,bt5)
    return markup

def atmen():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bt = KeyboardButton("Назад")
    markup.add(bt)
    return markup




    

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in admin:
        bot.send_message(message.chat.id,"Привет админ",reply_markup=admin_bt())
    elif bool(user_regis.get_user(message.from_user.id)):
        bot.send_message(message.chat.id,"qaytdinba bro \nSoraw bersen boladi",reply_markup=aliw())
    else:
        bot.send_message(
            message.chat.id,
            "Добро пожаловать! Для регистрации отправьте ваш номер телефона:",
            reply_markup=start_buttons()
        )




@bot.message_handler(content_types=['contact'])
def handle_contact(message):
        bot.send_message(
            message.chat.id,
            f"Регистрация завершена!\n"
            f"Ваш номер: {message.contact.phone_number}\n"
            f"ID: {message.from_user.id}\n"
            f"Имя: {message.from_user.first_name}",
            reply_markup=aliw()  # Убираем клавиатуру
        )
        user_regis.add_user(message.from_user.id,message.from_user.username,message.from_user.first_name,message.contact.phone_number)



@bot.message_handler(func=tekser)
def get(message):
    global user_chat_bas 
    if message.text == '❇️ Начат чат ❇️':
        user_chat_bas = 1
        bot.send_message(message.chat.id,"Можете задавать вапросы!",reply_markup=atmen())
    elif message.text == 'тех поддершка ☎️':
        bot.send_message(message.chat.id,"1182 – Горячая линия (общие жалобы)\n1103 – Энергетическая инспекция (подозрение на кражу)\n1310 – Энергия (аварийные отключения)")
    elif message.text == "👥о себе👥":
        bot.send_message(message.chat.id,"OpenEye:\nDoston\nRuslan\nAzamat\nShoxruh")
    elif message.text == 'Назад':
        user_chat_bas = 1
        bot.send_message(message.chat.id,"Главный меню",reply_markup=aliw())
    else:
        pass


@bot.message_handler(content_types=['text'])
def get_text(message):
    global user_chat_bas
    txt = message.text
    if message.from_user.id in admin:
        if txt == "Анализ 24ч":
            chat_historiy.day()
            file_path = 'chat_analytics_24h.png'
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Вот анализ 24ч")
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
        elif txt == "Анализ недели":
            chat_historiy.week()
            file_path = 'chat_analytics_7d.png'
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Вот анализ недели")
                
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
        elif txt == "Анализ месяца":
            chat_historiy.month()
            file_path = 'chat_analytics_30d.png'
            with open(file_path, 'rb') as photo:
                
                bot.send_photo(message.chat.id, photo, caption="Вот анализ месяца")
                
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
        elif txt == "Анализ года":
            chat_historiy.year()
            file_path = 'chat_analytics_1y.png'
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Вот анализ года")
            
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
        elif txt == "Полный Анализ Запрасов":
            chat_historiy.all()
            file_path = 'chat_analytics_all.png'
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Вот Полный Анализ Запрасов")
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
        elif txt =="Анализ по Категориям":
            bds.pie_chart()
            file_path = 'pie_chart.png'
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Анализ по Категориям")
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
    else:
        if user_chat_bas == 0:
            pass
        else:
            txt = test.generete_text(message.text)
            bot.send_message(message.chat.id,f"{txt}")
            ChatAnalytics().save_chat(message.from_user.id,message.text,txt)
            bds.kategoriyas(message.text,txt)




bot.infinity_polling()
