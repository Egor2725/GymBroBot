import telebot
from config import TOKEN


bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, "What's up bro?)")


@bot.message_handler()
def echo_all(message):
	bot.send_message(message.chat.id, message.text)


bot.infinity_polling()
