import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from handlers import router


bot = Bot(token='5046427784:AAE6GJrPNBEZV5sfRbCftJXAjt7jhRSz8bY')
dp = Dispatcher()
dp.include_router(router)

async def handle(request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response()

app = web.Application()
app.router.add_post("/webhook", handle)

async def on_startup(app):
    await bot.set_webhook(f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook")

app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
