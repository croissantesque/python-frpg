import fish_types
import random
import time
import sys




time_of_day = "day"
turn = 1
PERIOD_LENGTH = 12


quests= {
    "bridge_to_misty_creek": {"name": "The Bridge to Misty Creek", "rewards": {"skill": 1, "misty_creek": 1}, "requirements": {"wood_plank": 5}, "status": "hidden", "description": "The path to Misty Creek is blocked by a fallen bridge. Collect 5 Wood Planks and bring them to the Workshop so the bridge can be repaired.", "complete_description": "The path to Misty Creek is now open. You helped repair the bridge by delivering 5 wood planks." },
    "a_guide_by_scale": {"name": "A Guide By Scale", "rewards": {"skill": 2, "luck": 1.05, "shimmering_brook": 1}, "requirements": {"silverfin": 1, "iron_shard": 3, "glow_scale": 3}, "status": "hidden", "description": "The Silverfin's scales confirm the old tales of the Shimmering Brook upstream. You'll need climbing tools and Glow Scales to mark your way.", "complete_description": "Following the path upstream, you find the Shimmering Brook. The water sparkles with the same light as the Silverfin's scales - you've found the source."},
    "luminous_luck": {"name": "Luminous Luck", "rewards": {"money": 250, "luck": 1.08}, "requirements": {"glow_scale": 5}, "status": "hidden", "description": "Local legends say that collecting five Glow Scales and arranging them right brings fortune to the fisher. Perhaps there's truth to the tales?", "complete_description": "You've arranged the Glow Scales with the help of a local. They emit a soft, steady light as they hang around your neck. You feel luckier already!"}
}

zones = {
    "beginners_pond": True,
    "misty_creek": False,
    "shimmering_brook": False
}

crafting_recipes = {
    "iron_rod": {
        "name": "Iron Rod",
        "requirements": {
            "wood_plank": 3,
            "iron_shard": 5, 
            "magical_resin": 1
        },
        "cost": 200,
        "unlock_zone": "beginners_pond",  # Available from start
        "description": "A sturdy iron rod for tougher fish.",
        "type": "rod"
    },
    "azure_rod": {
        "name": "Azure Rod", 
        "requirements": {
            "azure_fin": 3,
            "river_pearl": 2,
            "iron_shard": 5
        },
        "cost": 300,
        "unlock_zone": "shimmering_brook",  # Only after unlocking this zone
        "description": "A magical rod that brings good fortune to your fishing.",
        'type': "rod"
    }
    # Add more recipes here as you create them
}

display_names = {
    "zones": {
        "beginners_pond": "Beginner's Pond",
        "misty_creek": "Misty Creek",
        "shimmering_brook": "Shimmering Brook"
    },

    "rods": {
        "wooden_rod": "Wooden Rod",
        "iron_rod": "Iron Rod",
        "azure_rod": "Azure Rod",
        "steel_rod": "Steel Rod",
        "silver_rod": "Silver Rod",
        "gold_rod": "Gold Rod",
        "mythic_rod": "Mythic Rod",
    },
    "drops": {
        "wood_plank": "Wood Plank",
        "iron_shard": "Iron Shard",
        "magical_resin": "Magical Resin",
        "river_pearl": "River Pearl",
        "azure_fin": "Azure Fin",
        "glow_scale": "Glow Scale"
    },
    "baits": {
        "worm": "worms",
        "insects": "insects",
        "shimmerbait": "shimmerbait",
        "glowworms": "glow worms",
        "golden_grubs": "golden grubs"
    },
    "zones": {
        "beginners_pond": "Beginner's Pond",
        "misty_creek": "Misty Creek",
        "shimmering_brook": "Shimmering Brook"
        
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
    "CrystalKoi": fish_types.CrystalKoi,
    "RapidfinTrout": fish_types.RapidfinTrout,
    "Carp": fish_types.BrookCarp,
    "Perch": fish_types.BrookPerch,
    "Shadowfin": fish_types.Shadowfin,
    "AzureGill": fish_types.AzureGill,
}

all_fish = list(fish_classes.keys())

rods = {
    "wooden_rod": (1, 1.1),
    "iron_rod": (1.5, 1),  
    "azure_rod": (1.3, 1.3),     
    "steel_rod": (2.5, 1),     

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
        "insects": 100,
        "shimmerbait": 300,
        "glowworms": 600,
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
        "crystal_koi": 350,
        "rapidfin_trout": 35,      
        "carp": 25,          
        "perch": 60,           
        "shadowfin": 45,        
        "azure_gill": 100,
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
    "Crystal Koi": "crystal_koi",
    "Rapidfin Trout": "rapidfin_trout",
    "Carp": "carp", 
    "Perch": "perch",
    "Shadowfin": "shadowfin",
    "Azure Gill": "azure_gill"

}

fish_displays = {
    "small_carp": "Small Carp",
    "minnow": "Minnow",
    "pond_perch": "Pond Perch",
    "night_goby": "Night Goby",
    "shimmerfin": "Shimmerfin",
    "trout": "Trout",
    "bass": "Bass",
    "glowfish": "Glowfish",
    "frogfish": "Frogfish",
    "silverfin": "Silverfin",
    "crystal_koi": "Crystal Koi",
    "rapidfin_trout": "Rapidfin Trout",
    "carp": "Carp",
    "perch": "Perch", 
    "shadowfin": "Shadowfin",
    "azure_gill": "Azure Gill"
}

class Player:
    def __init__(self, name):
        self.name = name
        self.fishing_skill = 1
        self.luck = 1
        self.gear = {"rod": "wooden_rod", "bait": "worm"}
        self.inventory = {"fish": {}, "coins": 0, "items": {}, "rods": {}, "baits": {"worm": 10}}
        self.completed_quests = set()
        self.zone = 0

def shop(player):
    while True:
        if time_of_day == "night":
            tprint("The Tackle Chest is closed during night hours. Come back tomorrow.", 0.02)
            return
        
        
        print(f"Money: ${player.inventory['coins']}")
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

            tprint(f'"Hey there, {player.name}! Take a look around, we sell bait in packs of 20."')
            
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

            tprint(f"{display_names['baits'][selected_bait].capitalize()}: costs ${selected_price}. Purchase? (y/n)", 0.01)
            confirm = input("> ")
            if confirm == "y":
                player.inventory["coins"] -= selected_price
                player.inventory["baits"][selected_bait] = player.inventory["baits"].get(selected_bait, 0) + 20
                print(f"Spent ${selected_price} on {display_names['baits'][selected_bait]}. Use [baits] outside of The Tackle Chest to equip.")
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

            for i, (fish_id, quantity) in enumerate(fish_inventory.items(), 1):
                fish_name = fish_displays.get(fish_id, fish_id)
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
            fish_external = fish_displays[selected_fish]
            quantity = fish_inventory[selected_fish]
            price_fetched = shop_prices["fish"][selected_fish] * fish_inventory[selected_fish]

            print(f"{fish_displays[selected_fish]}: Sell x{quantity} for ${price_fetched}? (y/n)")
            confirm = input("> ")
            
            if confirm == "y":
                del player.inventory["fish"][selected_fish]
                player.inventory["coins"] += price_fetched
                print(f"Sold {quantity} {fish_displays[selected_fish]} for ${price_fetched}.")
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
        stprint("[2] --- Quests")
        stprint("[0] --- Leave")

        main_select = input("> ")

        if main_select not in ["1", "2", "0"]: 
            tprint('"I don\'t got time for nonsense. Pick a real option."')
            continue
        if main_select == "0":
            tprint('"Off you go, then. Don\'t trip over the doorway."')
            return
        if main_select == "1":
            print("=== Crafting ===")
            stprint("[1] --- Rods")
            stprint("[0] --- Back\n")
            selection = input("> ")
            if selection not in ["1", "0"]:
                print("That's not an option...")
                continue

            if selection =="0":
                print("Returning...")
                continue

            if selection == "1":
                available_recipes = []
                for recipe_id, recipe_data in crafting_recipes.items():
                    if zones[recipe_data["unlock_zone"]] and recipe_data["type"] == "rod":
                        available_recipes.append((recipe_id, recipe_data))
                
                if not available_recipes:
                    tprint('"Nothing you can craft right now. Come back when you\'ve unlocked more areas."')
                    continue
                
                for i, (recipe_id, recipe_data) in enumerate(available_recipes, 1):
                    stprint(f"[{i}] --- {recipe_data['name']}")
                
                stprint("[0] --- Back")
                
                craft_select = input("> ")
                if craft_select == "0":
                    continue
                
                if not craft_select.isdigit():
                    print('That\'s not an option...')
                    continue
                if int(craft_select) < 1 or int(craft_select) > len(available_recipes):
                    print("That's not an option...")
                    continue
                
                selected_recipe_id, selected_recipe = available_recipes[int(craft_select) - 1]
                
                tprint(f"-- {selected_recipe['name']} --")
                time.sleep(0.05)
                stprint(f"Description: {selected_recipe['description']}")
                stprint(f"Requirements:")
                
                can_craft = True
                for item, quantity in selected_recipe["requirements"].items():
                    has_quantity = player.inventory["items"].get(item, 0)
                    status = "✓" if has_quantity >= quantity else "✗"
                    stprint(f" {status} {display_names['drops'][item]}: {has_quantity}/{quantity}")
                    if has_quantity < quantity:
                        can_craft = False
                
                stprint(f" {('✓' if player.inventory['coins'] >= selected_recipe['cost'] else '✗')} Coins: ${player.inventory['coins']}/${selected_recipe['cost']}")
                if player.inventory['coins'] < selected_recipe['cost']:
                    can_craft = False
                
                stprint("Craft? (y/n)")
                confirm = input("> ")
                
                if confirm == "y":
                    if can_craft:
                        for item, quantity in selected_recipe["requirements"].items():
                            player.inventory["items"][item] -= quantity
                            if player.inventory["items"][item] == 0:
                                del player.inventory["items"][item]
                        
                        player.inventory["coins"] -= selected_recipe["cost"]
                        
                        player.inventory["rods"][selected_recipe_id] = player.inventory["rods"].get(selected_recipe_id, 0) + 1
                        
                        craft_time = random.randint(5, 10)
                        tprint(f'Crafting ... (Est. {craft_time} seconds...)', 0.03)
                        time.sleep(craft_time)
                        tprint("Completed!", 0.02)
                        tprint(f'"There\'s your {selected_recipe["name"]}. Don\'t make me regret this."')
                    else:
                        print("You don't have the required materials!")
                else:
                    print("Crafting canceled.")

        if main_select == "2":
            print("=== Quests ===")
            print("\n --- Active ---")
            unlocked_quests_list = []
            active_quests = []
            complete_quests = []
            
           
            for i, (quest_id, quest_data) in enumerate(quests.items(), 1):
                if quest_data["status"] == "active": 
                    stprint(f"[{i}] --- {quest_data['name']}")
                    unlocked_quests_list.append(quest_id)
                    active_quests.append(quest_id)
                elif quest_data["status"] == "complete":
                    unlocked_quests_list.append(quest_id)
                    complete_quests.append(quest_id)
            
            if not unlocked_quests_list:
                print("No quests available.")
                print("[0] --- Back")
                input("> ")
                continue
            
            print("\n--- Completed ---")
            completed_display_list = []
            for quest_id, quest_data in quests.items():
                if quest_data["status"] == "complete":
                    completed_display_list.append(quest_id)
            
            for i, quest_id in enumerate(completed_display_list, len(active_quests) + 1):
                quest_data = quests[quest_id]
                stprint(f"[{i}] --- {quest_data['name']}")
            
            print("[0] --- Back")

            selection = input("> ")
            
            if not selection.isdigit():
                print("That's not an option...")
                continue
            
            selection = int(selection)
            if selection == 0:
                continue
            
            if selection < 1 or selection > len(unlocked_quests_list):
                print("That's not an option...")
                continue
            
            selected_quest = unlocked_quests_list[selection - 1]
            selected_quest_data = quests[selected_quest]
            
            if selected_quest in complete_quests:
                stprint(f"{selected_quest_data['name']} || Complete")
                stprint(f"{selected_quest_data['complete_description']}")
                stprint("Requirements:")
                for requirement, quantity in selected_quest_data['requirements'].items():
                    if requirement in display_names['drops']:
                        stprint(f" - {display_names['drops'][requirement]}: {quantity}/{quantity}")
                    elif requirement in fish_name_map:
                        stprint(f" - {requirement}: {quantity}/{quantity}")
                stprint("Rewards:")
                for reward, quantity in selected_quest_data["rewards"].items():
                    if reward == "skill": 
                        print(f" - +{quantity} Skill")
                    elif reward in zones:
                        print(f" - Unlocked {display_names['zones'][reward]}")
                    elif reward == "luck":
                        print(f" - x{quantity} Fishing Luck")
                    elif reward == "money":
                        print(f" - ${quantity}")
                tprint("Press <enter> to return...")
                input("> ")
                continue
            
            if selected_quest in active_quests:
                stprint(f"{selected_quest_data['name']} || Active")
                stprint(f"{selected_quest_data['description']}\n")
                stprint(f"Progress:")
                total_reqs = 0
                completed_reqs = 0
                
                for requirement, needed in selected_quest_data['requirements'].items():
                    total_reqs += 1
                    if requirement in display_names['drops']:
                        current = player.inventory['items'].get(requirement, 0)
                        stprint(f" - {display_names['drops'][requirement]} | {current}/{needed}")
                        if current >= needed: 
                            completed_reqs += 1
                    elif requirement in fish_name_map:
                        code_name = fish_name_map[requirement]
                        current = player.inventory['fish'].get(code_name, 0)
                        fish_display = [k for k,v in fish_name_map.items() if v == code_name][0]
                        stprint(f" - {fish_display} | {current}/{needed}")
                        if current >= needed: 
                            completed_reqs += 1
                
                if total_reqs == completed_reqs:
                    # confirm + complete!
                    tprint("You've fulfilled all the requirements! Finish Quest? (y/n) ")
                    confirm = input("> ")
                    if confirm.lower() == "y":
                        # Deduct resources
                        for requirement, quantity in selected_quest_data['requirements'].items():
                            if requirement in display_names["drops"]:
                                player.inventory['items'][requirement] = player.inventory['items'].get(requirement, 0) - quantity
                                if player.inventory['items'][requirement] <= 0:
                                    del player.inventory['items'][requirement]
                            elif requirement in fish_name_map:
                                fish_internal = fish_name_map[requirement]
                                player.inventory['fish'][fish_internal] -= quantity
                                if player.inventory['fish'][fish_internal] <= 0:
                                    del player.inventory['fish'][fish_internal]
                        
                        # Apply rewards
                        for reward, spec in selected_quest_data['rewards'].items():
                            if reward in zones:
                                zones[reward] = True
                            elif reward == "skill": 
                                player.fishing_skill += spec
                            elif reward == "luck":
                                player.luck = player.luck * spec
                            elif reward == "money":
                                player.inventory["coins"] += spec
                        
                        print("\n==============================")
                        stprint(f" QUEST COMPLETE: {selected_quest_data['name'].upper()} ")
                        print("==============================\n")
                        stprint(f"{selected_quest_data['complete_description']}\n")
                        stprint("Rewards:")
                        for reward, spec in selected_quest_data["rewards"].items():
                            if reward == "skill":
                                stprint(f" - +{spec} Fishing Skill")
                            elif reward == "luck":
                                stprint(f" - x{spec} Fishing Luck")
                            elif reward == "money": 
                                stprint(f" - +{spec} coins!")
                            elif reward in zones:
                                stprint(f" - {display_names['zones'][reward]} unlocked!")
                        
                        selected_quest_data['status'] = "complete"
                        player.completed_quests.add(selected_quest)
                    
                        stprint("\n==============================\n")
                        input("(press <enter> to continue)")
                    else:
                        continue

                
            
                

            

def inventory(player):
    stprint(f"\n-- {player.name}'s Inventory -- \n")
    
    print(f"Money: ${player.inventory['coins']}\n")

    print("Equipped Gear:")
    rod_code = player.gear["rod"]
    bait_code = player.gear["bait"]
    stprint(f"Rod: {display_names['rods'][rod_code]} (+{rods[rod_code]} skill)")
    stprint(f"Bait: {display_names['baits'][bait_code]} (+{baits[bait_code]} skill)\n")
    
    stprint("Fish:")
    for fish_key, quantity in player.inventory["fish"].items():
        fish_display = [k for k,v in fish_name_map.items() if v == fish_key][0]
        stprint(f"{fish_display} (x{quantity})")
    
    stprint("\nItems:")
    for item_name, quantity in player.inventory["items"].items():
        print(f"{display_names['drops'][item_name]} (x{quantity})")
    
    print("\nRods:")
    for rod, quantity in player.inventory["rods"].items():
        rod_display = display_names["rods"][rod]
        print(f"{rod_display} (x{quantity}) (+{rods[rod]} skill when equipped)")
    print("\nBaits:")
    for bait, quantity in player.inventory["baits"].items():
        bait_display = "Worms" if bait == "worm" else display_names["baits"][bait].capitalize()
        equip_mark = "[EQUIPPED]" if bait == player.gear["bait"] else ""
        if bait == "worm":
            print(f"{equip_mark} {bait_display}: Infinite")
        else:
            print(f"{equip_mark} {bait_display} (x{quantity})")


def switch_bait(player):
    print("--- Baits ---\n")
    for i, (bait, quantity) in enumerate(player.inventory["baits"].items(), 1):
        equip_mark = "[EQUIPPED]" if bait == player.gear["bait"] else ""
        bait_display = "Worms" if bait == "worm" else display_names["baits"][bait].capitalize()
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
                print(f"Switched bait to {display_names['baits'][selected_bait]} (x{player.inventory['baits'][selected_bait]} left)!")
            return
        
def switch_rods(player):
    print("\n--- Rods ---\n")
    print(f"Currently equipped: {player.gear['rod']}")
    for i, rod in enumerate(player.inventory["rods"].keys(), 1):
        luck_marker = f"(+{rods[rod][1]} fishing luck when equipped)" if rods[rod][1] > 1 else ""
        stprint(f"[{i}] --- {display_names['rods'][rod]} (+{rods[rod][0]} skill when equipped)  {luck_marker}")
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
    
    print(f"Successfully switched rod to {display_names['rods'][new_equip]}!")

def unlock_quest(quest):
    stprint("===== QUEST UNLOCKED =====")
    time.sleep(0.3)
    print("=" * 45)
    time.sleep(0.5)
    stprint(f"--- {quests[quest]['description']} ---")
    time.sleep(0.3)
    stprint(f"Visit the Workshop to learn more.")
    print("=" * 45)
    quests[quest]["status"] = "active"

def check_quest_unlocked(player):
    if 'night_goby' in player.inventory['fish'] and quests['bridge_to_misty_creek']['status'] == 'hidden':
        unlock_quest("bridge_to_misty_creek")
    if 'silverfin' in player.inventory['fish'] and quests['a_guide_by_scale']['status'] == 'hidden':
        unlock_quest("a_guide_by_scale")
    if zones["shimmering_brook"] and player.inventory['items'].get("glow_scale", 0) >= 1 and quests["luminous_luck"]["status"] == "hidden":
        unlock_quest("luminous_luck")
        



def switch_zone(player):
    print("\n--- Unlocked Fishing Zones ---\n")
    unlocked_list = []
    for i, (zone_code, status) in enumerate(zones.items(), 1):
        if status:
            current_marker = "[CURRENT ZONE]" if i == player.zone else ""
            stprint(f"[{i}] --- {current_marker} {display_names['zones'][zone_code]}")
            unlocked_list.append(zone_code)
    print("[0] --- Back\n")

    selection = input("> ")

    if not selection.isdigit():
        print("That's not an option...")
        return
    selection = int(selection)
    
    if selection < 0 or selection > len(unlocked_list):
        print("That's not an option...")
        return
    zone_display = display_names['zones'][unlocked_list[selection - 1]]
    player.zone = selection - 1
    tprint(f"You change fishing zones... Moved to {zone_display}")
    
    

def stprint(line, delay=0.07):
    print(line)
    time.sleep(delay)
    


def spawn_fish(player_zone, time_of_day):
    """Spawns a fish based on player zone and time of day"""
    possible_fish = []
    current_bait = player.gear["bait"]
    if player.inventory["baits"][current_bait] < 1:
        tprint(f"You're out of {display_names['baits'][current_bait]}! Visit The Tackle Shop to buy more or switch using [baits].")
        return
    player.inventory["baits"][current_bait] -= 1


    tprint(f"You flick the rod, and the line arcs over the water...", 0.007)
    time.sleep(random.uniform(1, 5))


    for fish_name, fish_class in fish_classes.items():
        fish_instance = fish_class()
        if player_zone in fish_instance.zones:
            possible_fish.append(fish_instance)
    
    if not possible_fish:
        return None
    
    og_roll = random.random()
    current_rod = player.gear['rod']
    effective_luck = player.luck * rods[current_rod][1]
    roll = og_roll * effective_luck
    roll = min(1, roll)
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


def reel_fish(player, fish, time_of_day, ticks=25, tick_duration=0.4):
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
    effective_skill = player.fishing_skill + rods[player.gear["rod"]][0] + baits[player.gear["bait"]]
    effective_difficulty = max(1, fish.difficulty - effective_skill)

    for i in range(ticks):
        progress_chance = min(0.8, 0.4 + (0.05 * effective_skill) - (0.03 * effective_difficulty))
        rng = random.random()
        if rng < progress_chance:
            progress = min(100, progress + random.randint(15,25))
        else: 
            progress = max(0, progress - random.randint(4, 8))
        filled = int(progress / 100 * bar_length)
        if random.random() < 0.1 and "jumpy" in fish.traits:
            progress = max(0, progress -  (progress * 0.20))
            print("The fish thrashes! You lose 20% of progress!")

        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"Reeling >>> [{bar}] {progress}%")

        if progress >= 100:
            print(random.choice(success_texts))
            internal = fish_name_map[fish.name]
            player.inventory["fish"][internal] = player.inventory["fish"].get(internal, 0) + 1
            return True

        time.sleep(tick_duration)
        i += 1

    print(random.choice(fail_texts))
    return False

def zone_info(player):
    print(f"\n--- Fish in {display_names['zones'][list(zones.keys())[player.zone]]} ---")
    
    current_zone_fish = []
    for fish_name, fish_class in fish_classes.items():
        fish_instance = fish_class()
        if player.zone in fish_instance.zones:
            current_zone_fish.append(fish_instance)
    
    if not current_zone_fish:
        print("No fish here at the moment.")
        return
    
    for fish in current_zone_fish:
        rarity = fish.day_rarity if time_of_day == "day" else fish.night_rarity
        print(f"- {fish.name} | {rarity}")



def tprint(text, delay=0.013):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

player_name = input("Enter your name: ")

player = Player(player_name.title())

tprint(f"Welcome, {player.name}. You stand at the edge of Beginner's Pond, where the sun glimmers off the rippling water and the air smells faintly of moss and adventure.", 0.02)
time.sleep(0.8)
tprint("Legends speak of rare fish that lurk in hidden corners, and treasures left behind by those who dared to fish here long ago.", 0.02)
time.sleep(0.7)
tprint("You'll start simple, but every catch brings experience, coins, and maybe even secrets waiting to be discovered.\n", 0.02)
time.sleep(0.5)
tprint("Here's what you can do to survive and thrive as a fisherman:")
time.sleep(0.3)
tprint(" - Type 'f' or 'fish' to cast your line and try your luck.", 0.004)
time.sleep(0.3)
tprint(" - Type 'inventory' to check your rods, baits, and catches.", 0.004)
time.sleep(0.3)
tprint(" - Type 'rods' to switch which rod you're using.", 0.004)
time.sleep(0.3)
tprint(" - Type 'baits' to switch baits or check your supply.", 0.004)
time.sleep(0.3)
tprint(" - Type 'shop' to visit The Tackle Chest and buy new baits, or sell your catches.", 0.004)
time.sleep(0.3)
tprint(" - Type 'workshop' to craft items or check your quests.", 0.004)
time.sleep(0.3)
tprint(" - Type 'zones' to switch between unlocked fishing areas.\n", 0.004)
time.sleep(0.8)
tprint("Your journey begins now. Keep an eye on the time of day, and remember: the right bait in the right place can make all the difference. Good luck, fisherman!", 0.023)

while True:
    turn+=1
    

    player.inventory["baits"]["worm"] += 1

    check_quest_unlocked(player)

    if turn >= PERIOD_LENGTH:
        turn = 1
        if time_of_day == "day":
            print(" --- The sun sets. Night falls.")
            time_of_day = "night"
            continue
        if time_of_day == "night":
            print(" --- The sun rises on the horizon. It's day.")
            time_of_day = "day"
            continue
    if time_of_day == "day": print(f"--- {(5 + turn - 1) % 24}:00 || Day")
    else: 
        if turn > 13: print(f"--- {(5 + turn - 1) % 24}:00 || Night")
        else: print(f" --- {5 + turn - 12}:00 || Night/Early Morning")

    command = input("> ")
    if command in ["f", "fish"]:
        fished = spawn_fish(player.zone, time_of_day)
        if fished == None: 
            print("Nothing but seaweed. Eugh.")

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
                                print(f"The {fished.name} dropped 1 {display_names['drops'][item]}!")
                                player.inventory["items"][item] = player.inventory["items"].get(item, 0) + 1
                                
                            continue
                    continue
    if command == "shop":
        shop(player)
        continue
    if command == "workshop":
        workshop(player)
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
    if command == "zones":
        switch_zone(player)
        continue
    if command == "info":
        zone_info(player)
        continue
