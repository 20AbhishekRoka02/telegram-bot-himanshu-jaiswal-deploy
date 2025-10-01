import logging
from telegram import Update, ForceReply, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    JobQueue
)
from dotenv import load_dotenv
import os

load_dotenv()

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
JOIN, FUN = range(2)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def get_bot_info(application) -> None:
    async with application:
        print(application.bot.name)
        print(application.bot.token)
        print(application.bot.users)
    
    
# Preparing for custom keyboard buttons
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from models import *
from crud import *

from database import engine
from sqlmodel import Session, SQLModel
SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = next(get_session())
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    lang = user.language_code
    print(user, user_id, username, first_name, last_name, lang)
    
    
    
    try:
        createLead(engine=db, lead=user)
    except Exception as e:
        print(e)
        logger.exception(e)
    
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please tell me. What brings you here?")
    """Send a message when the command /start is issued."""
    user = update.effective_user
  
    await update.message.reply_text('*Bold*, _italic_, *~strikethrough~*, __underline__', parse_mode='MarkdownV2')
    
    





async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


DEFAULT_START_MSG=InputMediaPhoto(media=open("app/images/1746050.jpg", mode="rb"), 
        caption="""
Hi, <user>!
*Lorem ipsum* dolor sit amet _consectetur_ adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas iaculis massa nisl malesuada lacinia integer nunc posuere ut hendrerit.

https://t.me/+DXEFtPl4rT1kMTdl

Once in a life time offer!
https://t.me/+DXEFtPl4rT1kMTdl
""", parse_mode="Markdown")

async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    # await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")
    await context.bot.send_media_group(
        chat_id=job.chat_id,
        media=[ InputMediaPhoto(media=open("app/images/1746050.jpg", mode="rb"), 
        caption="""
Hi, <user>!
*Lorem ipsum* dolor sit amet _consectetur_ adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas iaculis massa nisl malesuada lacinia integer nunc posuere ut hendrerit.

https://t.me/+DXEFtPl4rT1kMTdl

Once in a life time offer!
https://t.me/+DXEFtPl4rT1kMTdl
""".replace("<user>", job.name), parse_mode="Markdown")]
        )


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True



# to set schedule
async def set_timer(app) -> None:
    """Add a job to the queue."""
   
    with Session(engine) as db:
        leads = getLeads(engine=db)
    
    # this will run once only, need to set long term thing
    for lead in leads:
        try:
            # args[0] should contain the time for the timer in seconds
            due = float(10)
            if due < 0:
                # await update.effective_message.reply_text("Sorry we can not go back to future!")
                logger.warning("due < 0")
                return

            
            job_queue = app.job_queue
            job_queue.run_repeating(alarm, due, chat_id=lead['id'], name=" ".join([lead['first_name'], lead['last_name']]), data=due)
            print("scheduled!")


        except Exception as e:
            # await update.effective_message.reply_text("Usage: /set <seconds>")
            logger.exception(e)



async def sending_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    db = next(get_session())
    leads = getLeads(engine=db)
    
    for lead in leads:
        await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=[ InputMediaPhoto(media=open("app/images/1746050.jpg", mode="rb"), 
        caption="""
Hi, <user>!
*Lorem ipsum* dolor sit amet _consectetur_ adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas iaculis massa nisl malesuada lacinia integer nunc posuere ut hendrerit.

https://t.me/+DXEFtPl4rT1kMTdl

Once in a life time offer!
https://t.me/+DXEFtPl4rT1kMTdl
""".replace("<user>", " ".join([lead['first_name'], lead['last_name']])), parse_mode="Markdown")]
        )
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['TOKEN']).post_init(set_timer).build()
    
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("media", sending_media))
    application.add_handler(CommandHandler("cancel", cancel))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    
    