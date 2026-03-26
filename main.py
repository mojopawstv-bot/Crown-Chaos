import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, html
from aiogram.filters import Command

# --- IMPORTING YOUR MODULES ---
import database
import combat
import economy
import social
import dungeons

# 1. INITIALIZE BOT
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 2. SETUP DATABASE ON START
database.initialize_db()

# --- COMMAND: /start ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    player = database.get_player(message.from_user.id, message.from_user.first_name)
    welcome_text = (
        f"🏰 {html.bold('WELCOME TO THE KINGDOM')}\n\n"
        f"👤 Name: {player['name']}\n"
        f"💰 Gold: {player['gold']}\n"
        f"⚔️ Level: {player['level']}\n"
        f"🛡️ Rank: {player['rank']}\n\n"
        f"📜 Type /help to see the laws of the land!"
    )
    await message.answer(welcome_text, parse_mode="HTML")
    # Sync their UI Rank Tag
    await social.update_social_status(bot, message.chat.id, message.from_user.id)

# --- COMMAND: /duel ---
@dp.message(Command("duel"))
async def cmd_duel(message: types.Message):
    await combat.initiate_duel(bot, message)

# --- COMMAND: /STRIKE (Reaction Combat) ---
@dp.message(F.text == "/STRIKE")
async def cmd_strike(message: types.Message):
    await combat.resolve_strike(message)

# --- COMMAND: /explore (Dungeons) ---
@dp.message(Command("explore"))
async def cmd_explore(message: types.Message):
    result = await dungeons.start_exploration(message.from_user.id, message.from_user.first_name)
    await message.answer(result, parse_mode="HTML")

# --- COMMAND: /shop ---
@dp.message(Command("shop"))
async def cmd_shop(message: types.Message):
    shop_text = "🛒 **THE ROYAL ARMORY**\n\n"
    for key, item in economy.ITEMS.items():
        shop_text += f"• {item['name']}: {item['price']} Gold (Use `/buy {key}`)\n"
    await message.answer(shop_text, parse_mode="HTML")

# --- COMMAND: /buy ---
@dp.message(Command("buy"))
async def cmd_buy(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("❌ Usage: `/buy [item_name]`")
    
    result = await economy.process_transaction(message.from_user.id, args[1])
    await message.answer(result)
    # Sync rank in case they spent so much they dropped a rank!
    await social.update_social_status(bot, message.chat.id, message.from_user.id)

# --- GLOBAL ACTIVITY (Passive Income & Taxation) ---
@dp.message()
async def on_message(message: types.Message):
    if not message.text or message.text.startswith("/"):
        return

    # Players earn 10 gold per message, but the King taxes it!
    income, tax = await economy.collect_tax(message.from_user.id, 10)
    
    # Rare chance (1%) to find a random gem while chatting
    if random.random() < 0.01:
        await message.answer(f"💎 {message.from_user.first_name} found a rare gem in the chat! +500 Gold.")
        database.update_player(message.from_user.id, "gold", database.get_player(message.from_user.id)["gold"] + 500)

# 3. RUN THE ENGINE
async def main():
    print("🚀 KINGDOM ENGINE 2026: ACTIVE AND RUNNING")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")

