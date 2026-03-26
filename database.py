import json
import os
import logging

# This is where the 2,000+ players' data lives
DB_PATH = "kingdom_data.json"

def initialize_db():
    """Creates the vault if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"players": {}, "global": {"treasury": 50000, "king": None}}, f)

def load_data():
    """Opens the vault to read gold and ranks."""
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    """Locks the vault and saves progress."""
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def get_player(uid, name="Unknown Traveler"):
    """Finds a specific player or creates a new one."""
    db = load_data()
    uid = str(uid)
    if uid not in db["players"]:
        db["players"][uid] = {
            "name": name,
            "gold": 1000,
            "rank": "Peasant",
            "xp": 0,
            "level": 1,
            "inventory": [],
            "last_active": str(os.times())
        }
        save_data(db)
    return db["players"][uid]

def update_player(uid, key, value):
    """Changes a player's stats (like adding gold)."""
    db = load_data()
    if str(uid) in db["players"]:
        db["players"][str(uid)][key] = value
        save_data(db)

