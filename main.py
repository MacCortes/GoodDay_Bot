import os
from dotenv import load_dotenv
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import pandas as pd
import datetime
from pytz import timezone

##### Config
# load enviromental variables
load_dotenv()

# get bot token from .env file
BOT_TOKEN = os.getenv('BOT_TOKEN_GOODDAY')

# For logging how the bot it's doing
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

##### Load data
quotes = pd.read_csv('dataset/quotes.csv')

##### set timezone
time_zone = timezone('America/Mexico_City')

##### Marina's chat id
marina_chat_id = 872081518

##### 
async def send_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id, # context['chat_id'], 
        text='The bot is starting!')

##### Handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_daily(
        send_message, 
        datetime.time(hour=23, minute=45, second=0, tzinfo=time_zone), 
        chat_id=context._chat_id)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=f'Hi Marina, good day! {update.message.chat_id}')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers a greeting"""
    msg = update.message.text
    processed = msg.lower()

    if processed in ['hello', 'hi', 'hey']:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = quotes.loc[0, "quote"])
    else:
        await update.message.reply_text("Sorry, I don't understand you!")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # start handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hello", hello))

    # hello handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()