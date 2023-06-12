import telebot
import cv2
import os

bot = telebot.TeleBot("xxxx", parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Let's get the job done")

@bot.message_handler(commands=['help'])
def help_user(message):
    bot.send_message(message.from_user.id, "Все что я умею это обрабатывать картинки, пришли одну")
                     

@bot.message_handler(content_types=['text', 'document', 'audio'])
def message_respond(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет!")
    else:
        bot.send_message(message.from_user.id, "Я не понимаю. Напиши /help.")

@bot.message_handler(content_types=["photo"])
def handle_docs_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    global src
    src = 'D:\\Works\\Python\\Bot\\photos\\' + message.photo[1].file_id + ".png"
    
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Blur', callback_data='Blur'))
    markup.add(telebot.types.InlineKeyboardButton(text='Bitwise', callback_data='Bitwise'))
    markup.add(telebot.types.InlineKeyboardButton(text='Flame', callback_data='Flame'))
    markup.add(telebot.types.InlineKeyboardButton(text='Gray', callback_data='Gray'))
    
    bot.send_message(message.from_user.id, text="Какой фильтр вы хотите использовать?", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Применяю фильтр')
    
    img = cv2.imread(src)
    ksize = (10, 10)
    
    if call.data == 'Blur':
        img = cv2.blur(img, ksize)
    elif call.data == 'Bitwise':
        img = cv2.bitwise_not(img)
    elif call.data == 'Flame':
        ret,img = cv2.threshold(img, 127, 255, 0)
    elif call.data == 'Gray':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imwrite (src, img)
    bot.send_message(call.message.chat.id, "Фильтр применен!")
    bot.send_photo(call.message.chat.id, open(src, 'rb'))
   # os.remove(src)
    
bot.polling(none_stop=True, interval=1)