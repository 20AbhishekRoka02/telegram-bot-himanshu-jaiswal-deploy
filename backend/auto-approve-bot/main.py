import logging
import os
import json
from dotenv import load_dotenv
from telegram import Update, ChatMember
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

# Setup Logging functionality
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
DATA_FILE = "stored_messages.json"

# Ensure storage file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"data": []}, f)


# Prepare bot for storing data in DB.
from models import *
from crud import *

from database import engine
from sqlmodel import Session, SQLModel
SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session
        
        
        
# --- Helper functions ---
def save_message(message_name, chat_id, message_id):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    msgDict = {message_name: {"chat_id": chat_id, "message_id": message_id}}
    data["data"].append(msgDict)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {message_name}: chat_id={chat_id}, message_id={message_id}")

def load_messages():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# --- Conversation state ---
WAITING_FOR_MESSAGE = 1

# --- Command /addmsg ---
async def addmsg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != int(os.environ['BOT_OWNER_ID']):
        await update.message.reply_text("❌ Only the bot owner can use this command.")
        return ConversationHandler.END

    await update.message.reply_text(
        "Send me the message (text, sticker, photo, animation, or document) you want to store."
    )
    return WAITING_FOR_MESSAGE

# --- Capture the message from user ---
async def capture_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id

    # Use a unique message name
    message_name = f"usermsg_{user_id}_{message.message_id}"
    print("message: ", message.text)

    save_message(message_name, message.chat_id, message.message_id)
    await update.message.reply_text("Your message has been saved ✅")
    

    return ConversationHandler.END

# --- Cancel command ---
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled ❌")
    return ConversationHandler.END

# --- Handler: approve join request + forward stored messages ---
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    user_id = user.id

    # Approve the join request
    try:
        await context.bot.approve_chat_join_request(CHANNEL_ID, user_id)
        print(f"Approved join request for user {user_id}")
        await context.bot.send_message(
                chat_id=os.environ['BOT_OWNER_ID'],
                text=f"Approved join request for user {user_id} | {user.first_name} {user.last_name}"
            )
        
    except Exception as e:
        print(f"Error approving user {user_id}: {e}")
        return

    # Forward stored messages to the user
    stored_messages = load_messages()
    for msg in stored_messages["data"]:
        name = list(msg.keys())[0]
        try:
            await context.bot.forward_message(
                chat_id=user_id,
                from_chat_id=msg[name]['chat_id'],
                message_id=msg[name]['message_id']
            )
            print(f"Forwarded {name} to user {user_id}")
            
        except Exception as e:
            print(f"Error forwarding {name} to user {user_id}: {e}")
            
    # Save Leads to DB
    db = next(get_session())
    # user = update.message.from_user
    
    # user = await context.bot.get_chat(user.id)
    chat_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = str(user.username)
    lang = user.language_code
    isPremium = str(user.is_premium)
    print(user, user_id, username, first_name, last_name, lang, isPremium)
    # print(user)
    
    
    try:
        createLead(engine=db, lead=user)
    except Exception as e:
        print(e)
        # logger.exception(e)


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
            print(f"Sent farewell to {user.id} {user.first_name} {user.last_name}")
            await context.bot.send_message(
                chat_id=os.environ['BOT_OWNER_ID'],
                text=f"Sent farewell to {user.id} {user.first_name} {user.last_name}"
            )
        except Exception as e:
            print(f"Could not send farewell to {user.id}: {e}")
            
            
# --- Main ---
app = ApplicationBuilder().token(TOKEN).build()

# Conversation handler for /addmsg
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("addmsg", addmsg_command)],
    states={
        WAITING_FOR_MESSAGE: [
            MessageHandler(
                filters.TEXT & (~filters.Command(["/cancel"])) | filters.Sticker.ALL | filters.PHOTO | filters.ATTACHMENT | filters.ANIMATION,
                capture_message
            ),
            
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
app.add_handler(conv_handler)

# Handle join requests in the private channel
app.add_handler(ChatJoinRequestHandler(handle_join_request))

# Farewell user
app.add_handler(ChatMemberHandler(farewell_members, ChatMemberHandler.CHAT_MEMBER))

print("Bot running... Use /addmsg to store user messages + wait for join requests.")
app.run_polling()
