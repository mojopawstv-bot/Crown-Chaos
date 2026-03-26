import random
import asyncio
import database
import economy

# --- THE MONSTER MANUAL ---
# You can expand this list to 1,000 monsters to reach your goal
ENEMIES = {
    "Goblin": {"hp": 50, "atk": 10, "gold_min": 200, "gold_max": 500, "xp": 50},
    "Orc Raider": {"hp": 120, "atk": 25, "gold_min": 1000, "gold_max": 3000, "xp": 250},
    "Shadow Knight": {"hp": 300, "atk": 60, "gold_min": 5000, "gold_max": 12000, "xp": 1000},
    "Ancient Dragon": {"hp": 1000, "atk": 150, "gold_min": 50000, "gold_max": 150000, "xp": 5000}
}

# --- THE ROOM GENERATOR ---
LOCATIONS = [
    "the Damp Sewers 🐀", "the Whispering Woods 🌳", 
    "the Forgotten Mine ⚒️", "the Dragon's Nest 🌋",
    "the Cursed Graveyard 🪦"
]

async def start_exploration(user_id, user_name):
    """Generates a random adventure for the player."""
    player = database.get_player(user_id, user_name)
    loc = random.choice(LOCATIONS)
    
    # 20% chance of finding nothing, 70% chance of monster, 10% chance of pure treasure
    event_roll = random.random()
    
    if event_roll < 0.20:
        return f"🔦 You searched {loc} but found only dust and shadows."
    
    elif event_roll < 0.90:
        # Monster Encounter
        enemy_name, stats = random.choice(list(ENEMIES.items()))
        
        # Combat Calculation
        player_atk = 15 + (player["level"] * 5)
        player_def = 10 + (player["level"] * 3)
        
        # Did we win? (Simple high-speed logic)
        damage_taken = max(0, stats["atk"] - player_def)
        gold_won = random.randint(stats["gold_min"], stats["gold_max"])
        
        # Update Database via Economy (so King gets taxed!)
        net_gain, tax = await economy.collect_tax(user_id, gold_won)
        
        # Update XP
        new_xp = player["xp"] + stats["xp"]
        database.update_player(user_id, "xp", new_xp)
        
        return (
            f"⚔️ **BATTLE IN {loc.upper()}!**\n"
            f"You fought a **{enemy_name}**!\n\n"
            f"💥 Damage Taken: {damage_taken} HP\n"
            f"💰 Gold Found: {gold_won}\n"
            f"🏛️ Kingdom Tax: -{tax}\n"
            f"✨ XP Gained: +{stats['xp']}"
        )
    
    else:
        # Rare Treasure Room
        loot = random.randint(10000, 30000)
        await economy.collect_tax(user_id, loot)
        return f"💎 **TREASURY FOUND!**\nYou stumbled into a hidden vault in {loc} and looted {loot} Gold!"


