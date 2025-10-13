import asyncio
import logging
import os
import json
from dotenv import load_dotenv
from telegram import Update, ChatMember, InputMediaPhoto, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    ChatJoinRequestHandler,
    CommandHandler,
    ConversationHandler,
    ChatMemberHandler
)

# Importing Parse Mode
from telegram.constants import ParseMode

# Setup Logging functionality
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Global queue
# message_queue = asyncio.Queue()

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()
TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
DATA_FILE = "stored_messages.json"
logger.info("Loaded environment variables...")

# Ensure storage file exists
logger.info("Checking for message storage files")
if not os.path.exists(DATA_FILE):
    logger.info(f"storage file not exists, create one at {os.getcwd()}/{DATA_FILE}")
    with open(DATA_FILE, "w") as f:
        json.dump({"data": []}, f)
    logger.info(f"Storage file {os.getcwd()}/{DATA_FILE} created!")


# Prepare bot for storing data in DB.
logger.info("Importing models for database.")
from models import *

logger.info("Importing crud module for database database.")
from crud import *

logger.info("Importing database engine")
from database import engine
from sqlmodel import Session, SQLModel
SQLModel.metadata.create_all(engine)
logger.info("Created all metadata for DB Engine")

def get_session():
    with Session(engine) as session:
        yield session
        
from time import time
# Function to send all messages to a single user with delay
async def send_messages_to_user(bot, user_id, messages):
    keyboard = [ ["🔥 CLAIM YOUR FREE VIP 🔥"] ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
    
    for msg in messages["data"]:
        try:
            if msg["type"] == "photo":
                with open(msg["media"], "rb") as f:
                    # await bot.send_media_group(
                    #     chat_id=user_id,
                    #     media=[InputMediaPhoto(
                    #         media=f,
                    #         caption=msg["caption"],
                    #         parse_mode=ParseMode.MARKDOWN_V2
                    #     )]
                    # )
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=f,
                        caption=msg["caption"],
                        parse_mode= 'MarkdownV2',
                        reply_markup = reply_markup
                    )
            # wait 1 minute before next message
            # await asyncio.sleep(float(os.environ['DELAY']))
            await asyncio.sleep(int( 60 - (time() % 60)))
        
        except Exception as e:
            logger.error(f"Error sending message to {user_id}: {e}")



# --- Helper functions ---
def save_message(message_name, chat_id, message_id):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    msgDict = {message_name: {"chat_id": chat_id, "message_id": message_id}}
    data["data"].append(msgDict)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {message_name}: chat_id={chat_id}, message_id={message_id}")
    logger.info(f"Saved {message_name}: chat_id={chat_id}, message_id={message_id}")

def load_messages():
    logger.info("Loading saved messages from file")
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# --- Conversation state ---
WAITING_FOR_MESSAGE = 1

# --- Command /addmsg ---
async def addmsg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != int(os.environ['BOT_OWNER_ID']):
        await update.message.reply_text("❌ Only the bot owner can use this command.")
        logger.debug(f"{user_id} tried to use /addmsg command, who is not an Admin.")
        return ConversationHandler.END

    await update.message.reply_text(
        "Send me the message (text, sticker, photo, animation, or document) you want to store."
    )
    logger.info(f"{user_id} initiated the /addmsg command, and bot is waiting for the user to forward the message to be stored in file.")
    return WAITING_FOR_MESSAGE

# --- Capture the message from user ---
async def capture_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    # print("Message is: ", message)
    user_id = message.from_user.id

    # Use a unique message name
    logger.info(f"Created unique message name: usermsg_{user_id}_{message.message_id}")
    message_name = f"usermsg_{user_id}_{message.message_id}"
    # print("message: ", message.text)

    logger.info("Saving to message file.")
    # save_message(message_name, message.chat_id, message.message_id)
    await update.message.reply_text("Your message has been saved ✅")
    logger.info("Message saved!")
    return ConversationHandler.END

# --- Cancel command ---
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Cancelling an operation...")
    await update.message.reply_text("Operation cancelled ❌")
    return ConversationHandler.END

# --- Handler: approve join request + forward stored messages ---
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    user_id = user.id

    # Approve the join request
    try:
        await context.bot.approve_chat_join_request(CHANNEL_ID, user_id)
        logger.info(f"Approved join request for user {user_id}")
        print(f"Approved join request for user {user_id}")
        # await context.bot.send_message(
        #         chat_id=os.environ['BOT_OWNER_ID'],
        #         text=f"Approved join request for user {user_id} | {user.first_name} {user.last_name}"
        #     )
        # logger.info(f"Approved join request for user {user_id} | {user.first_name} {user.last_name} message sent to {os.environ['BOT_OWNER_ID']}")
        
        
    except Exception as e:
        logger.error(f"Error approving user {user_id}: {e}")
        print(f"Error approving user {user_id}: {e}")
        return

    # Sending stored messages to the user
    stored_messages = load_messages()
    
    # for msg in stored_messages["data"]:  
    #     try:
    #         if msg["type"] == "photo":
    #             await context.bot.send_media_group(
    #                 chat_id=user_id,
    #                 media = [
    #                     InputMediaPhoto(
    #                         media=open(msg["media"], mode="rb"),
    #                         caption=msg["caption"],
    #                         parse_mode="MarkdownV2"
    #                     )
    #                 ]
    #             )
    #         print(f"Sent message to {user.first_name} {user.last_name} {user_id}")
    #         logger.info(f"Sent message to {user.first_name} {user.last_name} {user_id}")
            
    #     except Exception as e:
    #         print(f"Error while sending the media: {e}")
    #         logger.error(f"Error while sending the media: {e}")
    
    try:
        # Start a separate task for this user
        asyncio.create_task(send_messages_to_user(context.bot, user_id, stored_messages))

    except Exception as e:
        print(f"Error while sending the media: {e}")
        logger.error(f"Error while sending the media: {e}")
    
    # await context.bot.send_message(chat_id=user_id, text="Welcome to the Channel!")
            
    # Save Leads to DB
    logger.info("Saving Leads to DB.")
    db = next(get_session())
    # user = update.message.from_user
    
    # user = await context.bot.get_chat(user.id)
    # chat_id = user.id
    # first_name = user.first_name
    # last_name = user.last_name
    # username = str(user.username)
    # lang = user.language_code
    # isPremium = str(user.is_premium)
    # print(user, user_id, username, first_name, last_name, lang, isPremium)
    # print(user)
    
    try:
        logger.info("Creating New Lead record in DB.")
        createLead(engine=db, lead=user)
    except Exception as e:
        # print(e)
        logger.error(f"Error occured: {e}, handled.")
        # logger.exception(e)

# test send
async def send_sample(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Sending stored messages to the user
    stored_messages = load_messages()
    
    for msg in stored_messages["data"]:
        
        try:
            if msg["type"] == "photo":
                await context.bot.send_media_group(
                    chat_id=os.environ['BOT_OWNER_ID'],
                    media = [
                        InputMediaPhoto(
                            media=open(msg["media"], mode="rb"),
                            caption=msg["caption"],
                    parse_mode=ParseMode.MARKDOWN_V2
                        )
                    ],
                )   
            # print(f"Sent message to {user.first_name} {user.last_name} {user_id}")
            # logger.info(f"Sent message to {user.first_name} {user.last_name} {user_id}")
            
        except Exception as e:
            print(f"Error while sending the media: {e}")
            logger.error(f"Error while sending the media: {e}")
            
# --- Handler for users leaving ---
async def farewell_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member
    user = chat_member.from_user
    old_status = chat_member.old_chat_member.status
    new_status = chat_member.new_chat_member.status

    # Check if user left or was kicked
    if old_status in [ChatMember.MEMBER, ChatMember.RESTRICTED] and new_status in [ChatMember.LEFT, ChatMember.BANNED]:
        # Send farewell message directly to user
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=f"Goodbye! We're sad to see you leave the channel."
            )
            # await update.message.reply_text(
                
            # )
            logger.info(f"{user.id} left/kicked from the channel.")
            
            await context.bot.send_message(
                chat_id=os.environ['BOT_OWNER_ID'],
                text=f"Sent farewell to {user.id} {user.first_name} {user.last_name}"
            )
            print(f"Sent farewell to {user.id} {user.first_name} {user.last_name}")
            logger.info(f"Sent farewell to {user.id} {user.first_name} {user.last_name}")
            
        except Exception as e:
            print(f"Could not send farewell to {user.id}: {e}")
            logger.error(f"Could not send farewell to {user.id}: {e}")
            
            
# --- Main ---
app = ApplicationBuilder().token(TOKEN).build()

# Start multiple workers (say 10-20)
# for _ in range(20):
#     asyncio.create_task(message_worker(app.bot))
    
    
# Conversation handler for /addmsg
# conv_handler = ConversationHandler(
#     entry_points=[CommandHandler("addmsg", addmsg_command)],
#     states={
#         WAITING_FOR_MESSAGE: [
#             MessageHandler(
#                 filters.TEXT & (~filters.Command(["/cancel"])) | filters.Sticker.ALL | filters.PHOTO | filters.ATTACHMENT | filters.ANIMATION,
#                 capture_message
#             ),
            
#         ]
#     },
#     fallbacks=[CommandHandler("cancel", cancel)]
# )
# app.add_handler(conv_handler)

# Handle join requests in the private channel
app.add_handler(ChatJoinRequestHandler(handle_join_request))

#app.add_handler(CommandHandler("send", send_sample))

# Farewell user
app.add_handler(ChatMemberHandler(farewell_members, ChatMemberHandler.CHAT_MEMBER))

print("Bot running... Use /addmsg to store user messages + wait for join requests.")
logger.info("Bot running... Use /addmsg to store user messages + wait for join requests.")
app.run_polling()
