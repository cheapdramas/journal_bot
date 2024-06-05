from aiogram import Bot,Dispatcher
from aiogram.filters import Command
import asyncio
import grequests
import routers.routes as router
import json
from request_funcs.requests import get_schedule
import ast

async def main():
    bot = Bot(token='6528370293:AAHNvlR9w0oxIeZt4k38qLTaVqUbbiq-P-U')
    
    dp = Dispatcher()
    dp.include_router(router.router)
    
    await dp.start_polling(bot)




if __name__ == '__main__':
    try:
        
        print('Бот вкл')
        asyncio.run(main())
    except:
        print('Бот викл')



