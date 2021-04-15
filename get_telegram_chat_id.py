import os
import telebot
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'], parse_mode='html')
# set up variable TELEGRAM_BOT_TOKEN in .env, change it to the token from your bot 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Your chat id {message.chat.id}')

# run this script and write some message to your bot - it will answer as upper ^^^^ with your chat id
bot.polling()
