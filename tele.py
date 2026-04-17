import telebot
from dotenv import load_dotenv
import os
from business_logic.data_logic import Data_Logic


load_dotenv()
# Replace 'YOUR_BOT_TOKEN_HERE' with the token you got from @BotFather
TOKEN = os.getenv("TELEGRAM_KEY")

bot = telebot.TeleBot(TOKEN)
myengine=Data_Logic()
# This decorator handles the /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_first_name = message.from_user.first_name
    bot.reply_to(message, f"Hello {user_first_name}! 👋 I'm your Python bot. How can I help you today?")

# This decorator handles all other text messages
@bot.message_handler(func=lambda message: message.text is not None and message.text.lower().startswith('@support'))
def handle_support(message):
   
    parts = message.text.split(' ', 1)
    
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Please include a message after @support. \nExample: `@support I need help with my account`", parse_mode="Markdown")
        return

    user_message = parts[1]
    
    # Log the support request
    print(f"New Ticket: {user_message}")
   
    bot.reply_to(message, "⏳ Processing your query, please wait a moment...")
    bot.reply_to(message,myengine.search_results(user_message),parse_mode="Markdown")


print("Bot is running...")
bot.infinity_polling()