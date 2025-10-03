import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    ChatJoinRequestHandler
)

# Load environment variables
load_dotenv()
TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
BOT_OWNER_ID = int(os.environ['BOT_OWNER_ID'])
DATA_FILE = "stored_messages.json"

# Ensure storage file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"data":list()}, f)

# --- Helper functions ---
def save_message(message_name, chat_id, message_id):
    msgDict = dict()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    msgDict[message_name] = {"chat_id": chat_id, "message_id": message_id}
    data["data"].append(msgDict)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {message_name}: chat_id={chat_id}, message_id={message_id}")

def load_messages():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# --- Handler: store messages from bot owner ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # print("Inside handle_message")
    message = update.message
    
    # print(f"message.from_user.id\ntype: {type(message.from_user.id)} and \nvalue: {message.from_user.id}")
    # print(f"BOT_OWNER_ID\ntype: {type(BOT_OWNER_ID)} and \nvalue: {BOT_OWNER_ID}")

    try:
        # Only capture messages from bot owner
        if message.from_user.id != BOT_OWNER_ID:
            return
    except Exception as e:
        print(e)
        return

    save_message(str(message.chat_id), message.chat_id, message.message_id)
    await message.reply_text("Premium sticker saved ✅")
    # if message.sticker:
    #     save_message("premium_sticker", message.chat_id, message.message_id)
    #     await message.reply_text("Premium sticker saved ✅")
    # elif message.text:
    #     save_message("text_message", message.chat_id, message.message_id)
    #     await message.reply_text("Text message saved ✅")

# --- Handler: approve join request + forward stored messages ---
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    user_id = user.id

    # Approve the join request
    try:
        await context.bot.approve_chat_join_request(CHANNEL_ID, user_id)
        print(f"Approved join request for user {user_id}")
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

# --- Main ---
app = ApplicationBuilder().token(TOKEN).build()

# Store messages sent by bot owner
app.add_handler(MessageHandler(filters.ALL, handle_message))

# Handle join requests in the private channel
app.add_handler(ChatJoinRequestHandler(handle_join_request))

print("Bot running... Send it messages to store + wait for join requests.")
app.run_polling()
