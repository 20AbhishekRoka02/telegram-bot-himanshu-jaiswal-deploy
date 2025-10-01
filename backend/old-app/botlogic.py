import logging
from telegram import Update
from telegram.ext import (
    # ApplicationBuilder,
    # CommandHandler,
    ContextTypes,
    # ConversationHandler,
    # MessageHandler,
    # filters,
    # CallbackQueryHandler,
)
# from dotenv import load_dotenv
# import os

# load_dotenv()

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

# async def get_bot_info(application) -> None:
#     async with application:
#         print(application.bot.name)
#         print(application.bot.token)
#         print(application.bot.users)
    
    
# Preparing for custom keyboard buttons
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    lang = user.language_code
    print(user, user_id, username, first_name, last_name, lang)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please tell me. What brings you here?")
    
    
    # """Sends a message with three inline buttons attached."""
    # keyboard = [
    #     [
    #         InlineKeyboardButton("Join The Channel!", callback_data=str(JOIN)),
    #         InlineKeyboardButton("Just for fun!", callback_data=str(FUN)),
    #     ],
    #     # [InlineKeyboardButton("Option 3", callback_data="3")],
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)
    # await update.message.reply_text("I'm a bot, please tell me. What brings you here?", reply_markup=reply_markup)





# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Cancels and ends the conversation."""
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation.", user.first_name)
#     await update.message.reply_text(
#         "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
#     )

#     return ConversationHandler.END



# async def join_grp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     query = update.callback_query
#     msg =  query.data
#     print("message: ", msg)
#     print("chat_id: ", update.effective_chat.id) # Here I get the chat_id
#     try:
#         await context.bot.send_message(text="So, u want to join a group", chat_id=update.effective_chat.id)
#     except Exception as e:
#         pass
#     return START_ROUTES

# async def have_fun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     query = update.callback_query
#     message =  await query.answer()
#     print("message: ", message)
#     await update.message.reply_text("So, u want to HAVE FUN!")
#     return END_ROUTES


# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     await query.answer()

#     await query.edit_message_text(text=f"Selected option: {query.data}")

# if __name__ == '__main__':
#     application = ApplicationBuilder().token(os.environ['TOKEN']).build()
    
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start", start)],
    #     states={
    #         START_ROUTES: [
    #             CallbackQueryHandler(join_grp, pattern="^" + str(JOIN) + "$"),
    #             CallbackQueryHandler(have_fun, pattern="^" + str(FUN) + "$")
    #         ],
    #         END_ROUTES: [
    #             CallbackQueryHandler(start, pattern = "^"+ str(JOIN) +"$"),
    #             CallbackQueryHandler(cancel, pattern = "^"+ str(FUN) +"$"),
    #         ]
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )
    
    # application.add_handler(conv_handler)
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CallbackQueryHandler(join_grp, pattern="^" + str(JOIN) + "$"))
    # application.add_handler(CallbackQueryHandler(have_fun, pattern="^" + str(FUN) + "$"))
    # application.add_handler(CommandHandler("cancel", cancel))
    
    # print(application.bot)
    
        
    
    # application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    
    # To get bot info
    # import asyncio 
    # asyncio.run(get_bot_info(application=application))
    