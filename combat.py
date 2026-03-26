import random
import asyncio
from aiogram import types, html
import database  # This connects to the 'Accountant' we just made

# --- THE REFLEX SYSTEM (2026 NATIVE) ---
active_duels = {}

async def initiate_duel(bot, message: types.Message):
    """Starts a professional 1v1 challenge."""
    if not message.reply_to_message:
        return await message.answer("🤺 **ERROR:** To challenge a rival, you must REPLY to their message!")

    challenger = message.from_user
    defender = message.reply_to_message.from_user

    if challenger.id == defender.id:
        return await m.answer("⚔️ You cannot duel your own shadow, Knight.")

    # Create a unique ID for this specific fight
    duel_id = f"{challenger.id}_{defender.id}"
    active_duels[duel_id] = {"status": "waiting", "start_time": asyncio.get_event_loop().time()}

    msg = await message.answer(
        f"⚔️ **DUEL ISSUED!**\n{html.bold(challenger.first_name)} vs {html.bold(defender.first_name)}\n\n"
        f"Prepare your blades... The signal comes soon!", 
        parse_mode="HTML"
    )

    # Wait 3-6 seconds to build tension
    await asyncio.sleep(random.randint(3, 6))

    # MARCH 2026: The 'Force Draft' vibrates the phone and puts /STRIKE in the bar
    for uid in [challenger.id, defender.id]:
        try:
            await bot.send_message_draft(chat_id=message.chat.id, user_id=uid, text="/STRIKE")
        except:
            pass # Standard fallback if user has drafts disabled

    await msg.edit_text("🔥 **STRIKE NOW!**\nFirst one to hit SEND wins!")
    active_duels[duel_id]["status"] = "active"

async def resolve_strike(message: types.Message):
    """Calculates who won and distributes the gold/XP."""
    user_id = message.from_user.id
    player = database.get_player(user_id, message.from_user.first_name)
    
    # Check if this user is actually in an active duel
    found_duel = None
    for d_id, data in active_duels.items():
        if str(user_id) in d_id and data["status"] == "active":
            found_duel = d_id
            break
    
    if found_duel:
        # Victory Logic
        loot = random.randint(500, 2500)
        xp_gain = 100
        
        # Update Database
        new_gold = player["gold"] + loot
        new_xp = player["xp"] + xp_gain
        database.update_player(user_id, "gold", new_gold)
        database.update_player(user_id, "xp", new_xp)
        
        # Level Up Logic (Every 1000 XP = 1 Level)
        new_level = (new_xp // 1000) + 1
        if new_level > player["level"]:
            database.update_player(user_id, "level", new_level)
            await message.answer(f"🎊 **LEVEL UP!** {message.from_user.first_name} is now Level {new_level}!")

        # End the duel
        del active_duels[found_duel]
        
        await message.answer(
            f"💥 **CRITICAL HIT!**\n{html.bold(message.from_user.first_name)} was faster!\n"
            f"💰 Loot: {loot} Gold\n✨ XP: +{xp_gain}",
            parse_mode="HTML"
        )

