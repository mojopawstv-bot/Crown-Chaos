import random
import database

# --- THE SHOP CATALOG (Professional Scaling) ---
# Each item has a price and a power-up effect
ITEMS = {
    "steel_sword": {"name": "Steel Sword 🗡️", "price": 5000, "atk": 10},
    "iron_shield": {"name": "Iron Shield 🛡️", "price": 3000, "def": 15},
    "royal_cloak": {"name": "Royal Cloak 🧥", "price": 15000, "luck": 5},
    "mana_potion": {"name": "Mana Potion 🧪", "price": 500, "hp": 50}
}

async def process_transaction(user_id, item_key):
    """Professional Shop Logic: Checks gold and adds items to inventory."""
    player = database.get_player(user_id)
    item = ITEMS.get(item_key)
    
    if not item:
        return "❌ Item not found in the Royal Armory."
    
    if player["gold"] < item["price"]:
        return f"❌ You lack the gold! You need {item['price'] - player['gold']} more Gold."
    
    # Update Player's Gold and Inventory
    new_gold = player["gold"] - item["price"]
    database.update_player(user_id, "gold", new_gold)
    
    current_inv = player.get("inventory", [])
    current_inv.append(item["name"])
    database.update_player(user_id, "inventory", current_inv)
    
    return f"✅ Purchased {item['name']}! Your remaining balance is {new_gold} Gold."

async def collect_tax(user_id, amount):
    """The 'King's Tax' system. Takes a percentage for the Treasury."""
    db = database.load_data()
    tax_rate = db["global"].get("tax_rate", 0.05) # Default 5% tax
    
    tax_amount = int(amount * tax_rate)
    net_income = amount - tax_amount
    
    # Add to King's Treasury
    db["global"]["treasury"] += tax_amount
    database.save_data(db)
    
    # Update Player's Wealth
    player = database.get_player(user_id)
    new_gold = player["gold"] + net_income
    database.update_player(user_id, "gold", new_gold)
    
    return net_income, tax_amount

def get_treasury_status():
    """Shows the current wealth of the Kingdom."""
    db = database.load_data()
    return db["global"]["treasury"]

