import fish_types
import random
import time
import sys

time_of_day = "day"
turn = 1
period_length = random.randint(6,12)

zones = [
    "Starting Pond",
    "Misty Pond",
    "Shimmering Brook"
]

item_displays = {
    "rods": {
        "wooden_rod": "Wooden Rod",
        "iron_rod": "Iron Rod",
        "steel_rod": "Steel Rod",
        "silver_rod": "Silver Rod",
        "gold_rod": "Gold Rod",
        "mythic_rod": "Mythic Rod",
    },
    "drops": {
        "wood_plank": "Wood Plank",
        "iron_shard": "Iron Shard",
        "magical_resin": "Magical Resin",
    },
    "baits": {
        "worm": "worms",
        "insects": "insects",
        "shimmerbait": "shimmerbait",
        "glowworms": "glow worms",
        "golden_grubs": "golden grubs"
    }
}


fish_classes = {
    "SmallCarp": fish_types.SmallCarp,
    "Minnow": fish_types.Minnow,
    "PondPerch": fish_types.PondPerch,
    "NightGoby": fish_types.NightGoby,
    "Shimmerfin": fish_types.Shimmerfin,
    "Trout": fish_types.Trout,
    "Bass": fish_types.Bass,
    "Glowfish": fish_types.Glowfish,
    "Frogfish": fish_types.Frogfish,
    "Silverfin": fish_types.Silverfin,
    "CrystalKoi": fish_types.CrystalKoi
}

all_fish = list(fish_classes.keys())

rods = {
    "wooden_rod": 1,
    "iron_rod": 2,       
    "steel_rod": 4,     
    "silver_rod": 5,    
    "gold_rod": 7,      
    "mythic_rod": 10  
}

baits = {
    "worm": 0,           # default, no bonus
    "insects": 1,      #cost money from here on
    "shimmerbait": 2,   
    "glowworms": 3,    
    "golden_grubs": 5  
}

shop_prices = {
    "bait": {
        "insects": 120,
        "shimmerbait": 350,
        "glowworms": 650,
        "golden_grubs": 1300
    },

    "fish": {
        "small_carp": 5,
        "minnow": 5,
        "pond_perch": 20, 
        "night_goby": 25,
        "shimmerfin": 130,
        "trout": 10,
        "bass": 30,
        "glowfish": 80,
        "frogfish": 30,
        "silverfin": 50,
        "crystal_koi": 350
    }

}

fish_name_map = {
    "Small Carp": "small_carp",
    "Minnow": "minnow",
    "Pond Perch": "pond_perch",
    "Night Goby": "night_goby",
    "Shimmerfin": "shimmerfin",
    "Trout": "trout",
    "Bass": "bass",
    "Glowfish": "glowfish",
    "Frogfish": "frogfish",
    "Silverfin": "silverfin",
    "Crystal Koi": "crystal_koi"
}


class Player:
    def __init__(self, name):
        self.name = name
        self.fishing_skill = 1
        self.luck = 1
        self.gear = {"rod": "wooden_rod", "bait": "worm"}
        self.inventory = {"fish": {}, "coins": 0, "items": {}, "rods": {}, "baits": {"worm": 10}}
        self.completed_quests = set()
        self.location = 0

def shop(player):
    while True:
        if time_of_day == "night":
            tprint("The Tackle Chest is closed during night hours. Come back tomorrow.", 0.02)
            return
        
        
        print(f"Money: ${player.inventory["coins"]}")
        print("=== The Tackle Chest ===")
        print("=" * 40)
        stprint("  [1] --- Buy Bait")
        stprint("  [2] --- Sell Fish")
        stprint("  [0] --- Exit Shop")

        main_selection = input("> ")
        if main_selection == "1":

            bait_options = {
                "1": "insects",
                "2": "shimmerbait",
                "3": "glowworms",
                "4": "golden_grubs"
            }

            tprint(f'"Hey there, {player.name}! Take a look around, we sell bait in packs of 50."')
            
            stprint(f"[1] --- Insects")
            stprint(f"[2] --- Shimmerbait")
            stprint(f"[3] --- Glow Worms")
            stprint(f"[4] --- Golden Grubs")
            stprint(f"[0] --- Back")
            

            bait_selection = input("> ")
            if bait_selection not in ["1", "2", "3", "4", "0"]:
                print("That's not an option...")
                continue

            if bait_selection == "0":
                continue


            selected_bait = bait_options[bait_selection]
            selected_price = shop_prices["bait"][selected_bait]

            if player.inventory["coins"] < selected_price:
                tprint('"Sorry mate, but it seems like you\'ve not enough money."')
                continue

            tprint(f"{item_displays["baits"][selected_bait].capitalize()}: costs ${selected_price}. Purchase? (y/n)", 0.01)
            confirm = input("> ")
            if confirm == "y":
                player.inventory["coins"] -= selected_price
                player.inventory["baits"][selected_bait] = player.inventory["baits"].get(selected_bait, 0) + 50
                print(f"Spent {selected_price} on {item_displays["baits"][selected_bait]}. Use [baits] outside of The Tackle Chest to equip.")
                tprint(f'"There ya go, {player.name}! Have fun with \'em!"')
                continue
            else:
                tprint('"Alright, maybe next time, eh?"')
                continue
            
            
            
        elif main_selection == "2":
            tprint('"Ah, looking to sell some of your catches? You\'ve found the right place!"')
            
            fish_inventory = player.inventory["fish"]

            if not fish_inventory: 
                tprint('"Hmm, seems like you don\'t have any fish to sell. Go catch some first!"')
                continue
            
            fish_list = list(fish_inventory.keys())

            for i, (fish_name, quantity) in enumerate(fish_inventory.items(), 1):
                print(f"[{i}] --- {fish_name} (x{quantity})")
                time.sleep(0.04)
            print("[0] --- Back")


            fish_selection = input("> ")

            if fish_selection == "0":
                continue
            
            elif not fish_selection.isdigit():
                print("That's not an option...")
                continue
            elif int(fish_selection) < 1 or int(fish_selection) > len(fish_list):
                print("That's not an option... ")
                continue


            selected_fish = fish_list[int(fish_selection) - 1]
            quantity = fish_inventory[selected_fish]
            fish_code = fish_name_map[selected_fish]
            price_fetched = shop_prices["fish"][fish_code] * fish_inventory[selected_fish]

            print(f"{selected_fish}: Sell x{quantity} for ${price_fetched}? (y/n)")
            confirm = input("> ")
            
            if confirm == "y":
                del player.inventory["fish"][selected_fish]
                player.inventory["coins"] += price_fetched
                print(f"Sold {quantity} {selected_fish} for {price_fetched}.")
                tprint('"There\'s your cash, kid! Good doing business with ya!"')
                continue
            else: 
                print("Sale canceled.")
                tprint('"Nah? Maybe another time, then."')
                continue

        else: 
            tprint(f'"Come back again, {player.name}! Don\'t let those fish bite without you."')
            return

def workshop(player):
    if time_of_day == "day":
        print("The Workshop's closed during the day. Come back tonight?")
        return
    while True:
        print("=== Workshop ===")
        print("=" * 40)
        tprint('"Whaddya want? it\'s late, kid."')
        
        stprint("[1] --- Crafting")
        stprint("[0] --- Leave")

        main_select = input("> ")

        if main_select not in ["1", "0"]: 
            tprint('"I don\'t got time for nonsense. Pick a real option."')
            continue
        if main_select == "0":
            tprint('"Off you go, then. Don\'t trip over the doorway."')
            return
        if main_select == "1":
            print("=== Crafting ===")
            stprint("[1] --- Iron Rod")
            stprint("[0] --- Back")

            craft_select = input("> ")
            if craft_select not in ["1", "0"]:
                print('"What? Stop mumbling, kid!"')
                continue
            if craft_select == "0":
                continue
            
            if craft_select == "1":
                tprint("-- Iron Rod --")
                time.sleep(0.05)
                stprint(f"Requires:")
                stprint(f"3 Wooden Plank (You have x{player.inventory["items"].get("wooden_plank", 0)})")
                stprint(f"5 Iron Shard (You have x{player.inventory["items"].get("iron_shard", 0)})")
                stprint(f"1 Magical Resin (You have x{player.inventory["items"].get("magical_resin", 0)})")
                stprint(f"Crafting fee: $200 (You have ${player.inventory["coins"]})")
                stprint("Craft? (y/n)")
                confirm = input("> ")
                
                if confirm == "y":
                    if player.inventory["coins"] >= 200 and player.inventory["items"].get("wooden_plank", 0) >= 3 and player.inventory["items"].get("iron_shard", 0) >= 5 and player.inventory["items"].get("magical_resin", 0) >= 1:
                        player.inventory["rods"]["iron_rod"]  = player.inventory["rods"].get("iron_rod", 0) + 1
                        player.inventory["items"]["wooden_plank"] -= 3
                        player.inventory["items"]["iron_shard"] -= 5
                        player.inventory["items"]["magical_resin"] -= 1
                        player.inventory["coins"] -= 200
                        if player.inventory["items"]["wooden_plank"] == 0: del player.inventory["items"]["wooden_plank"]
                        if player.inventory["items"]["iron_shard"] == 0: del player.inventory["items"]["iron_shard"]
                        if player.inventory["items"]["magical_resin"] == 0: del player.inventory["items"]["magical_resin"]

                        craft_time = random.randint(5, 10)
                        tprint(f'Crafting ... (Est. {craft_time} seconds...')
                        time.sleep(craft_time)
                        tprint("Completed!")
                        tprint('"Hmph. Took you long enough, but here\'s your Iron Rod. Try not to break it on the first fish!"')
                        continue
                    else: 
                        print("You don't have the resources for this!")
                        continue
                else: 
                    print("Crafting canceled.")
                    continue


def inventory(player):
    stprint(f"\n-- {player.name}'s Inventory -- \n")
    
    print(f"Money: ${player.inventory["coins"]}\n")

    print("Equipped Gear:")
    rod_code = player.gear["rod"]
    bait_code = player.gear["bait"]
    stprint(f"Rod: {item_displays["rods"][rod_code]} (+{rods[rod_code]} skill)")
    stprint(f"Bait: {item_displays["baits"][bait_code]} (+{baits[bait_code]} skill)\n")
    
    stprint("Fish:")
    for fish_name, quantity in player.inventory["fish"].items():
        stprint(f"{fish_name} (x{quantity})")
    
    stprint("\nItems:")
    for item_name, quantity in player.inventory["items"].items():
            print(f"{item_displays["drops"][item_name]} (x{quantity})")

    print("\nRods:")
    for rod, quantity in player.inventory["rods"].items():
        rod_display = item_displays["rods"][rod]
        print(f"{rod_display} (x{quantity}) (+{rods[rod]} skill when equipped)")
    print("\nBaits:")
    for bait, quantity in player.inventory["baits"].items():
        
        bait_display = item_displays["baits"][bait]

        if bait == player.gear["bait"]:
            if bait == "worm": print("[EQUIPPED] Worms: Infinite")
            else: print(f"[EQUIPPED] {bait_display.capitalize()} (x{quantity})")
            continue
        
        if bait == "worm": print("Worms: infinite")
        else:
            print(f"{bait_display.capitalize()} (x{quantity})")

def switch_bait(player):
    print("--- Baits ---\n")
    for i, (bait, quantity) in enumerate(player.inventory["baits"].items(), 1):
        equip_mark = "[EQUIPPED]" if bait == player.gear["bait"] else ""
        bait_display = "Worms" if bait == "worm" else item_displays["baits"][bait].capitalize()
        if bait == "worm":
            stprint(f"[{i}] {equip_mark} --- {bait_display} (Infinite)")    
        else:
            stprint(f"[{i}] {equip_mark} --- {bait_display} (x{quantity})")   
    stprint("[0] --- Cancel")

    baits_list = list(player.inventory["baits"].keys())
    selection = input("> ")
    if selection == "0":
        print("Canceled.")
        return
    else:
        if not selection.isdigit():
            print("That's not an option...")
            return
        selection = int(selection)

        if selection < 0 or selection > len(baits_list):
                print("That's not an option...")
                return
        else:
            selected_bait = baits_list[selection - 1]
            player.gear["bait"] = selected_bait
            if selected_bait == "worm":
                print("Switched bait to worms (infinite)!")
            else:
                print(f"Switched bait to {item_displays['baits'][selected_bait]} (x{player.inventory['baits'][selected_bait]} left)!")
            return
        
def switch_rods(player):
    print("\n--- Rods ---\n")
    print(f"Currently equipped: {player.gear["rod"]}")
    for i, rod in enumerate(player.inventory["rods"].keys(), 1):
        stprint(f"[{i}] --- {item_displays['rods'][rod]} (+{rods[rod]} skill when equipped)")
    print("[0] --- Cancel")
    
    rods_list = list(player.inventory["rods"].keys())
    selection = input("> ")

    if not selection.isdigit():
        print("That's not an option...")
        return
    
    selection = int(selection)

    if selection < 0 or selection > len(rods_list):
        print("That's not an option...")
        return

    if selection == 0:
        print("Canceled.")
        return


    current_equip = player.gear["rod"]   
    new_equip = rods_list[selection - 1]
    player.inventory["rods"][current_equip] = player.inventory["rods"].get(current_equip, 0) + 1
    player.inventory["rods"][new_equip] -= 1
    player.gear["rod"] = new_equip
    if player.inventory["rods"][new_equip] == 0:
        del player.inventory["rods"][new_equip]
    
    print(f"Successfully switched rod to {item_displays['rods'][new_equip]}!")
    
        


def stprint(line, delay=0.07):
    print(line)
    time.sleep(delay)
    


def spawn_fish(player_location, time_of_day):
    """Spawns a fish based on player location and time of day"""
    possible_fish = []
    current_bait = player.gear["bait"]
    if player.inventory["baits"][current_bait] > 1:
        tprint(f"You're out of {item_displays['baits'][current_bait]}! Visit The Tackle Shop to buy more or switch using [baits].")
        return
    player.inventory["baits"][current_bait] -= 1


    tprint(f"You flick the rod, and the line arcs over the water...", 0.007)
    time.sleep(random.uniform(1, 5))


    for fish_name, fish_class in fish_classes.items():
        fish_instance = fish_class()
        if player_location in fish_instance.zones:
            possible_fish.append(fish_instance)
    
    if not possible_fish:
        return None
    
    roll = random.random()
    if roll < 0.65: rolled_type = "Common"
    elif roll < 0.8: rolled_type = "Uncommon"
    elif roll < 0.85: rolled_type = "Rare"
    elif roll < 0.865: rolled_type = "Very Rare"
    elif roll < 0.8664: rolled_type = "Extremely Rare"
    elif roll < 0.8669: rolled_type = "Legendary"
    else: rolled_type = None

    fish_in_roll = []
    for fish_instance in possible_fish:
        if time_of_day == "day":
            if rolled_type == fish_instance.day_rarity:
                fish_in_roll.append(fish_instance)
        elif time_of_day == "night":
            if rolled_type == fish_instance.night_rarity:
                fish_in_roll.append(fish_instance)

    if len(fish_in_roll) == 0: rolled_type = None

    if rolled_type == None:
        return None
    else: 
        fish_spawned = random.choice(fish_in_roll)
        return fish_spawned

def reel_fish(player, fish, time_of_day, ticks=20, tick_duration=0.4):
    """Attempt to reel in a fish, uses random, skewed by difficulty + player skill"""
    if random.randint(1, 100) <= fish.escape_chance(player.fishing_skill, time_of_day):
        print(f"Oop- the fish wriggles free!")
        return False
    
    success_texts = [
        f"Success! You've landed a {fish.name}!",
        "Well done! That's one catch for the books.",
        f"Got it! The {fish.name} is yours.",
        "Victory! The fish is finally in your hands."
        ]
    
    fail_texts = [
        "Snap! Looks like you underestimated it.",
        "The line breaks! It's gone.",
        "The line snaps! Unlucky..."
    ]
    
    
    progress = 0
    bar_length = 20
    effective_skill = player.fishing_skill + rods[player.gear["rod"]] + baits[player.gear["bait"]]
    for i in range(ticks):
        progress_chance = min(0.75, (effective_skill / (fish.difficulty * 2)))
        rng = random.random()
        if rng < progress_chance:
            progress = min(100, progress + random.randint(10,20))
        else: 
            progress = max(0, progress - random.randint(5, 10))
        filled = int(progress / 100 * bar_length)

        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"Reeling >>> [{bar}] {progress}%")

        if progress >= 100:
            print(random.choice(success_texts))
            player.inventory["fish"][fish.name] = player.inventory["fish"].get(fish.name, 0) + 1
            return True

        time.sleep(tick_duration)
        i += 1

    print(random.choice(fail_texts))
    return False


def tprint(text, delay=0.013):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

player_name = input("Enter your name: ")

player = Player(player_name.title())
while True:

    player.inventory["baits"]["worm"] += 1
    if turn >= period_length:
        turn = 1
        if time_of_day == "day":
            print(" --- The sun sets. Night falls.")
            time_of_day = "night"
            period_length = random.randint(6,12)
            continue
        if time_of_day == "night":
            print(" --- The sun rises on the horizon. It's day.")
            time_of_day = "day"
            period_length = random.randint(6,12)
            continue

    command = input("> ")
    if command in ["f", "fish"]:
        fished = spawn_fish(player.location, time_of_day)
        if fished == None: 
            print("Nothing but seaweed. Eugh.")
            turn += 1
            
            continue
        else: 
            rarity = fished.day_rarity if time_of_day == "day" else fished.night_rarity
            tprint(f"Tug - something's on the line! It's a {fished.name} ({rarity}) || Press <enter> to reel... ", 0.008)
            if input("> ") == "":
                reeled = reel_fish(player, fished, time_of_day)
                if reeled:
                    if hasattr(fished, "drops"):
                        for item, rarity in fished.drops.items():
                            if random.random() <= rarity:
                                print(f"The {fished.name} dropped 1 {item_displays["drops"][item]}!")
                                player.inventory["items"][item] = player.inventory["items"].get(item, 0) + 1
                                
                            turn += 1
                            continue
                    turn += 1
                    continue
    if command == "shop":
        shop(player)
        turn += 1
        continue
    if command == "workshop":
        workshop(player)
        turn += 1
        continue
    if command == "inventory":
        inventory(player)
        continue

    if command == "baits":
        switch_bait(player)
        continue

    if command == "rods":
        switch_rods(player)
        continue