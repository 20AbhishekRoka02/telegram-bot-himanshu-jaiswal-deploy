from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlmodel import SQLModel, Session
from . import models, crud

# from .database import engine
# SQLModel.metadata.create_all(engine)

from typing import Annotated, Optional


from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
import os
from dotenv import load_dotenv
load_dotenv()

from .botlogic import start 
WEBHOOK_URL = "https://127.0.0.1:80/webhook"

app = FastAPI()
application = ApplicationBuilder().token(os.environ['TOKEN']).build()

# Add handlers to your bot
application.add_handler(CommandHandler("start", start))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# def get_session():
#     with Session(engine) as session:
#         yield session

@app.on_event("startup")
async def startup():
    await application.bot.set_webhook(WEBHOOK_URL)
    
@app.get("/")
async def root():
    return {"message":"Hello, World!"}

# print("Hello, Uvicorn World!")

# Coding the Telegram



# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# # set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)
# logger = logging.getLogger(__name__)

# async def get_bot_info(application) -> None:
#     async with application:
#         print(application.bot.name)
#         print(application.bot.token)
#         print(application.bot.users)


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     user_id = user.id
#     first_name = user.first_name
#     last_name = user.last_name
#     username = user.username
#     lang = user.language_code
#     print(user, user_id, username, first_name, last_name, lang)
    
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please tell me. What brings you here?")
    
    
    
    
    
    
# application = ApplicationBuilder().token(os.environ['TOKEN']).build()
# application.add_handler(CommandHandler("start", start))

# application.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
    pass