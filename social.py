import database
from aiogram import Bot, types, html

# --- THE ROYAL HIERARCHY ---
# Professional titles that appear in the Telegram UI
RANKS = {
    "Peasant": {"tag": "𝐏𝐄𝐀𝐒𝐀𝐍𝐓 🪵", "min_gold": 0},
    "Citizen": {"tag": "𝐂𝐈𝐓𝐈𝐙𝐄𝐍 🛡️", "min_gold": 5000},
    "Knight": {"tag": "𝐊𝐍𝐈𝐆𝐇𝐓 ⚔️", "min_gold": 25000},
    "Baron": {"tag": "𝐁𝐀𝐑𝐎𝐍 🏰", "min_gold": 100000},
    "King": {"tag": "𝐒𝐎𝐕𝐄𝐑𝐄𝐈𝐆𝐍 👑", "min_gold": 1000000}
}

async def update_social_status(bot: Bot, chat_id, user_id):
    """MARCH 2026: Physically changes the user's tag in the group chat."""
    player = database.get_player(user_id)
    current_gold = player["gold"]
    
    # Calculate the new rank based on wealth
    new_rank = "Peasant"
    for rank, data in sorted(RANKS.items(), key=lambda x: x[1]['min_gold'], reverse=True):
        if current_gold >= data["min_gold"]:
            new_rank = rank
            break
    
    # Save the new rank to the database
    database.update_player(user_id, "rank", new_rank)
    
    # API 9.5: Change the 'Member Tag' (Requires Bot to be Admin)
    try:
        tag_text = RANKS[new_rank]["tag"]
        await bot.set_chat_member_tag(chat_id=chat_id, user_id=user_id, tag=tag_text)
        return new_rank
    except Exception as e:
        # Fallback if bot is not admin or tag limit reached
        return f"{new_rank} (Tag Sync Failed: {e})"

async def issue_decree(bot: Bot, chat_id, king_name, message_text):
    """The King's global announcement system."""
    decree_msg = (
        f"📜 {html.bold('ROYAL DECREE FROM THE THRONE')}\n"
        f"👑 {html.bold(king_name)} has spoken:\n\n"
        f"「 {message_text} 」\n\n"
        f"⚡️ {html.italic('All subjects must obey or face the dungeons.')}"
    )
    return decree_msg

