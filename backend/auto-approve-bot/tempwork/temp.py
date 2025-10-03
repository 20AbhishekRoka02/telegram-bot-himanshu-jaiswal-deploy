from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes, ChatMemberHandler

from telegram.ext import CommandHandler

import os
from dotenv import load_dotenv
load_dotenv()
# TOKEN = "YOUR_BOT_TOKEN"

# This will handle new join requests
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    
    # Auto approve request
    await request.approve()
    
    # Get user details
    chat_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    
    # Send log to your own chat (replace with your admin chat_id)
    # ADMIN_CHAT_ID = 5824018470  
    
    if user.is_premium:
        msg = f"✅ Approved {first_name} {last_name} (@{username}) | chat_id: {chat_id} is a PREMIUM User."
    else:
        msg = f"✅ Approved {first_name} {last_name} (@{username}) | chat_id: {chat_id} is a NOT PREMIUM User."
    await context.bot.send_message(chat_id=os.environ['ADMIN_CHAT_ID'], text=msg)

    # Optional: Send welcome message to user
    # await context.bot.send_message(chat_id=chat_id, text=f"Welcome {first_name} {last_name} to the channel!")
    await context.bot.send_message(chat_id=chat_id, text=f"Welcome to the channel!")
    


async def track_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    status = result.new_chat_member.status
    user = result.from_user

    # if status == "member":
    #     await context.bot.send_message(
    #         chat_id=user.id,
    #         # text=f"👋 Welcome {user.first_name} {user.last_name} to the channel!"
    #         text=f"👋 Welcome to the channel!"
    #     )
    if status in ["left", "kicked"]:  # User left or got removed
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        chat_id = user.id
        
        if user.is_premium:
            msg = f"😲 {first_name} {last_name} (@{username}) recently LEFT the Channel | chat_id: {chat_id} is a PREMIUM User."
        else:
            msg = f"😲 {first_name} {last_name} (@{username}) recently LEFT the Channel | chat_id: {chat_id} is a NOT PREMIUM User."
        
        await context.bot.send_message(chat_id=os.environ['ADMIN_CHAT_ID'], text=msg)
        
        await context.bot.send_message(
            chat_id=user.id,
            # text=f"😢 Goodbye {user.first_name} {user.last_name}, we’ll miss you!"
            text=f"😢 Goodbye, we’ll miss you!"
        )



from promotionals import promotion1
async def sendmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    # await context.bot.send_message(
    #         chat_id=user.id,
    #         # text=f"😢 Goodbye {user.first_name} {user.last_name}, we’ll miss you!"
    #         text=f"😢 Goodbye, we’ll miss you!"
    #     )
    
    await context.bot.send_media_group(
        chat_id=user.id,
        media=[ promotion1 ]
        )
        
def main():
    app = Application.builder().token(os.environ['TOKEN']).build()

    # Handle new join requests
    app.add_handler(ChatJoinRequestHandler(auto_approve))

    # Track users
    app.add_handler(ChatMemberHandler(track_member, ChatMemberHandler.CHAT_MEMBER))
    
    # Test Send
    app.add_handler(CommandHandler("sendmsg", sendmsg))
    
    print("Bot is running... Auto-approving join requests ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
