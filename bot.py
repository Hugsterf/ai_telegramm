from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import Router, types
from websockets.sync.client import connect
import logging
import asyncio

bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()
router = Router()
dp.include_router(router)

async def send_to_websocket(text: str) -> str:
    try:
        with connect("ws://localhost:8000") as websocket:
            websocket.send(f"/ai {text}")
            response = websocket.recv()
            return response
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        return "Ошибка соединения с сервером"

@router.message(Command("ai"))
async def handle_ai_request(message: types.Message):
    question = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    
    if not question:
        await message.answer("Пожалуйста, укажите вопрос после команды /ai")
        return
    
    wait_msg = await message.answer("⏳ Ожидайте ответа нейросети...")
    
    try:
        response = await send_to_websocket(question)
        
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=wait_msg.message_id,
            text=response
        )
    except Exception as e:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=wait_msg.message_id,
            text=f"Произошла ошибка: {str(e)}"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")