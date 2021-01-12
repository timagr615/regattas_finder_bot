from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor

from config import (BOT_TOKEN, SKIP_UPDATES)
from db.database import engine
from db import models

models.Base.metadata.create_all(bind=engine)

storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
executor = Executor(dp, skip_updates=SKIP_UPDATES)
