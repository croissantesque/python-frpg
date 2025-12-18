import fish_types
import random
import time
import sys
import math
try:
    import msvcrt  # Windows
    def flush_input():
        while msvcrt.kbhit():
            msvcrt.getch()
except ImportError:
    import termios  # Linux / Mac
    def flush_input():
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


time_of_day = "day"
turn = 1
PERIOD_LENGTH = 12

setting_lines = False
caught_while_setlines = {
    "fish": {},
    "drops": {}
}
quests= {
    "bridge_to_misty_creek": {
        "name": "The Bridge to Misty Creek",
        "rewards": {"skill": 1, "misty_creek": 1}, 
        "requirements": {"wood_plank": 3}, 
        "status": "hidden", 
        "description": "The path to Misty Creek is blocked by a fallen bridge. Collect 3 Wood Planks and bring them to the Workshop so the bridge can be repaired.",
        "complete_description": "The path to Misty Creek is now open. You helped repair the bridge by delivering 5 wood planks."
    },

    "pond_master": {
        "name": "Pond Master",
        "rewards": {"skill": 1, "money": 150, "luck": 0.03},
        "requirements": {"small_carp": 1, "minnow": 1, "pond_perch": 1, "night_goby": 1, "shimmerfin": 1},
        "status": "hidden",
        "description": "Catch and deliver one of each of Beginner Pond's fish. Prove your foundational fishing skills!",
        "complete_description": "You've mastered the Beginner's Pond! Your basic technique is now flawless, making all future fishing easier."
    },

    "the_shack": {
        "name": "The Old Wooden Shack",
        "rewards": {"luck": 0.04, "shack": 1,},
        "requirements": {"iron_shard": 3, "wood_plank": 3, "glow_scale": 2},
        "status": "hidden",
        "description": "Overlooking Beginner's Pond sits a weathered old shack, abandoned but sturdy. With a few repairs and a touch of light from Glow Scales, it could become your personal home to rest between casts.",
        "complete_description": "You've patched up the Old Wooden Shack! It now stands cozy and warm by the pond's edge. For the first time, the waters feel a little like home. (Unlocks [home] and [setlines] commands)"
        
    },

    "creek_master": {
        "name": "Misty Creek Master",
        "rewards": {"skill": 1, "money": 250, "luck": 0.04},
        "requirements": {"small_carp": 1, "minnow": 1, "trout": 1, "bass": 1, "glowfish": 1, "frogfish": 1, "silverfin": 1},
        "status": "hidden",
        "description": "Conquer Misty Creek's diverse fish. Each fish teaches a different angling technique.", 
        "complete_description": "You've mastered the marine life of Misty Creek! Your versatility as a fisherman is notable."
    },

    "a_guide_by_scale": {
        "name": "A Guide By Scale", 
        "rewards": {"skill": 2, "luck": 0.04, "shimmering_brook": 1}, 
        "requirements": {"silverfin": 1, "iron_shard": 3, "glow_scale": 3}, 
        "status": "hidden", 
        "description": "The Silverfin's scales confirm the old tales of the Shimmering Brook upstream. You'll need climbing tools and Glow Scales to mark your way.", 
        "complete_description": "Following the path upstream, you find the Shimmering Brook. The water sparkles with the same light as the Silverfin's scales - you've found the source."
    },

    
    "brook_master": {
        "name": "Shimmering Brook Master",
        "rewards": {"skill": 1, "money": 350, "luck": 0.03},
        "requirements": {"minnow": 1, "rapidfin_trout": 1, "carp": 1, "perch": 1, "shadowfin": 1, "azure_gill": 1, "crystal_koi": 1},
        "status": "hidden", 
        "description": "The Shimmering Brook ecosystem requires specialized knowledge. Catch 'em all!",
        "complete_description": "You've unraveled the mysteries of Shimmering Brook! Your precision has sharpened."
    },

    "luminous_luck": {
        "name": "Luminous Luck", 
        "rewards": {"money": 250, "luck": 0.05}, 
        "requirements": {"glow_scale": 5}, 
        "status": "hidden", 
        "description": "Local legends say that collecting five Glow Scales and arranging them right brings fortune to the fisher. Perhaps there's truth to the tales?", 
        "complete_description": "You've arranged the Glow Scales with the help of a local. They emit a soft, steady light as they hang around your neck. You feel luckier already!"
    },
    
    "crystal_lake_expedition": {
        "name": "The Crystal Lake Expedition", 
        "rewards": {"skill": 2, "crystal_lake": 1},
        "requirements": {"crystal_koi": 1, "glow_scale": 5, "river_pearl": 4},
        "status": "hidden",
        "description": "The Crystal Koi proves the legends of a pristine high-altitude lake. You'll need light sources and purification pearls to reach it.",
        "complete_description": "You've reached the legendary Crystal Lake! The waters are so clear you can see straight to the bottom."
    },

    "lake_master": {
        "name": "Lake Master",
        "rewards": {"skill": 2, "money": 300, "luck": 0.08},
        "requirements": {"moonlight_guppy": 1, "deepwater_sturgeon": 1, "prism_trout": 1, "abyssal_angler": 1, "lunar_trout": 1},
        "status": "hidden",
        "description": "Master the powerful Crystal Lake by catching each of its mystical inhabitants.",
        "complete_description": "You are a conqueror of Crystal Lake! An achievement notable at even the highest ranks of fishermen."
    },

    "lake_guardian": {
        "name": "The Lake Guardian",
        "rewards": {"skill": 2, "money": 800, "luck": 0.1},
        "status": "hidden",
        "requirements": {"ghost_carp": 1},
        "description": "The lake's legendary mystery awaits. Prove your worth by catching the fabled Ghost Carp.",
        "complete_description": "You've finally captured the rumoured guardian of the lake! You are a true master of these waters."
    }
}

zones = {
    "beginners_pond": True,
    "misty_creek": False,
    "shimmering_brook": False,
    "crystal_lake": False
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
        "unlock_zone": "beginners_pond",  
        "description": "A sturdy iron rod for tougher fish.",
        "type": "rod"
    },
    "azure_rod": {
        "name": "Azure Rod", 
        "requirements": {
            "azure_fin": 4,
            "river_pearl": 4,
            "iron_shard": 3
        },
        "cost": 300,
        "unlock_zone": "shimmering_brook",  
        "description": "A magical rod that brings good fortune to your fishing.",
        'type': "rod"
    },
        "crystal_rod": {
        "name": "Crystal Rod",
        "requirements": {
            "crystal_shard": 3,
            "moonstone": 2, 
            "magical_resin": 2
        },
        "cost": 500,
        "unlock_zone": "crystal_lake",
        "description": "A rod made from Crystal Lake materials, excellent for finding rare fish.",
        "type": "rod"
    },
    "lunar_lure": {
        "name": "Bait Pack (Lunar Lure)",
        "requirements": {
            "glow_scale": 3,
            "moonstone": 1,
            "river_pearl": 1
        },
        "cost": 100,
        "unlock_zone": "crystal_lake",
        "description": "Glows with moonlight, attracting rare nocturnal fish. Comes in packs of 25.",
        "type": "bait",
        "quantity": 25,
        "crafted_item": "lunar_lure"
    },
    "insects": {
        "name": "Bait Pack (Insects)",
        "requirements": {
            "small_carp": 7,
            "minnow": 3,
            "wood_plank": 1
        },
        "cost": 50,
        "unlock_zone": "beginners_pond",
        "description": "Crafts 35 Insects bait. A useful way to recycle common catches.",
        "type": "bait",
        "quantity": 35,
        "crafted_item": "insects"

    }
}

fish_descriptions = {
    "small_carp": "It nibbles on everything it finds. Its constant chewing strengthens its surprisingly tough teeth.",
    "minnow": "This tiny fish swims at incredible speeds. It appears as a silver blur in the water. [Fast]",
    "pond_perch": "Known for its energetic leaps from the water. Each jump can reach surprising heights. [Jumpy]",
    "night_goby": "Active only after dark. It uses its whiskers to find food in complete darkness. [Nocturnal]",
    "shimmerfin": "Its scales shimmer with rainbow colors. Many seek it for its beautiful appearance. [Glows]",
    "trout": "A powerful swimmer that thrives in cold water. It battles fiercely when hooked. [Fast]",
    "bass": "This aggressive predator strikes without warning. Its large mouth can swallow prey whole. [Strong]",
    "glowfish": "It glows with mystical blue light. The glow intensifies during nighttime hours. [Glows]",
    "frogfish": "Camouflages perfectly with river bottoms. It hops along the floor like a frog. [Camouflage] [Jumpy]",
    "silverfin": "So slippery it's nearly impossible to hold. It escapes from most predators with ease. [Evasive]",
    "crystal_koi": "Considered a living jewel. Its translucent body sparkles like fine crystal. [Glows]",
    "rapidfin_trout": "Its fins move so fast they hum. This helps it swim against strong currents. [Fast] [Strong]",
    "carp": "A bottom-feeder that stirs up mud. It grows larger with each passing year. [Strong]",
    "perch": "Its sharp dorsal spines contain mild venom. Handle this feisty fish with care! [Jumpy]",
    "shadowfin": "Blends perfectly with dark waters. It strikes when prey least expects it. [Camouflage] [Evasive]",
    "azure_gill": "Emits a soft blue glow when excited. Known for its spectacular jumping displays. [Glows] [Jumpy]",
    "moonlight_guppy": "Tiny fish that absorb moonlight, creating a soft glow. They move in shimmering schools through the dark waters. [Glows]",
    "deepwater_sturgeon": "Ancient bottom-feeders with armored plates. They've adapted to the crushing pressures of the lake's deepest trenches. [Strong] [Camouflage]",
    "prism_trout": "Their scales refract light into rainbow patterns. Each movement creates a dazzling display of colors in the clear water. [Glows] [Evasive]",
    "abyssal_angler": "Uses a natural bioluminescent lure to attract prey in the dark depths. Its sharp teeth can cut through fishing line. [Glows] [Strong]",
    "lunar_trout": "Synchronized with the moon's cycles. Becomes more active and energetic during full moon nights. [Nocturnal] [Jumpy]",
    "ghost_carp": "So pale it's nearly transparent. Legends say it's the spirit of the lake itself, rarely seen by mortal eyes. [Camouflage]"
}

weather_types = ["Clear", "Rainy", "Stormy", "Foggy"]
current_weather = "Clear"
weather_timer = 48
weather_announces = {
    "Clear": "The sky's clear, and the waters sparkle.",
    "Foggy": "The gentle mist thickens into an oppressive fog...",
    "Rainy": "A downpour begins - nocturnal fish are easier to fish!",
    "Stormy": "Dark clouds roll in - a heavy storm's arrived..."
}
weather_descs = {
    "Clear": "(Luck boosted!)",
    "Rainy": "(Nocturnal fish more active!)",
    "Foggy": "(Fish are more slippery...)",
    "Stormy": "(Conditions are bad, luck decreased!)"
}

display_names = {
    "zones": {
        "beginners_pond": "Beginner's Pond",
        "misty_creek": "Misty Creek",
        "shimmering_brook": "Shimmering Brook",
        "crystal_lake": "Crystal Lake"
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
        "glow_scale": "Glow Scale",
        "crystal_shard": "Crystal Shard",
        "moonstone": "Moonstone",
        "spectral_fin": "Spectral Fin"
    },
    "baits": {
        "worm": "worms",
        "insects": "insects",
        "shimmerbait": "shimmerbait",
        "glowworms": "glow worms",
        "golden_grubs": "golden grubs"
    },
    "decor": {
        "cozy_rug": "Cozy Woven Rug",
        "oil_lantern": "Brass Oil Lantern",
        "wooden_chair": "Rustic Wooden Chair", 
        "small_aquarium": "Small Glass Aquarium",
        "wall_shelf": "Oak Wall Shelf", 
        "fishing_trophy_case": "Mounted Trophy Case",
        "plush_armchair": "Plush Armchair",
        "glowing_plant_pot": "Glowing Plant Pot",
        "large_aquarium": "Large Floor Aquarium",
        "crystal_chandelier": "Crystal Chandelier",
        "legendary_trophy_plaque": "Legendary Trophy Plaque",
        "riverside_landscape_painting": "Riverside Landscape Painting"

    }
}



fish_classes = {
    "small_carp": fish_types.SmallCarp,
    "minnow": fish_types.Minnow,
    "pond_perch": fish_types.PondPerch,
    "night_goby": fish_types.NightGoby,
    "shimmerfin": fish_types.Shimmerfin,
    "trout": fish_types.Trout,
    "bass": fish_types.Bass,
    "glowfish": fish_types.Glowfish,
    "frogfish": fish_types.Frogfish,
    "silverfin": fish_types.Silverfin,
    "crystal_koi": fish_types.CrystalKoi,
    "rapidfin_trout": fish_types.RapidfinTrout,
    "carp": fish_types.BrookCarp,
    "perch": fish_types.BrookPerch,
    "shadowfin": fish_types.Shadowfin,
    "azure_gill": fish_types.AzureGill,
    "moonlight_guppy": fish_types.MoonlightGuppy,
    "deepwater_sturgeon": fish_types.DeepwaterSturgeon, 
    "prism_trout": fish_types.PrismTrout,
    "abyssal_angler": fish_types.AbyssalAngler,
    "lunar_trout": fish_types.LunarTrout,
    "ghost_carp": fish_types.GhostCarp
}
fish_class_inv = {v: k for k,v in fish_classes.items()}
all_fish = list(fish_classes.keys())

rods = {
    "wooden_rod": (1, 0.05),
    "iron_rod": (1.5, 0),  
    "azure_rod": (1.4, 0.1),     
    "steel_rod": (2.2, 0),     
    "crystal_rod": (2, 0.17),
}

baits = {
    "worm": 0,          
    "insects": 1,      
    "shimmerbait": 2,   
    "glowworms": 3,    
    "golden_grubs": 5,
    "lunar_lure": 2
}
bait_luck = {
    "worm": 0, 
    "insects": 0.05,
    "shimmerbait": 0.13,
    "glowworms": 0.20,
    "golden_grubs": 0.25
}

decor_descs = {
    "cozy_rug": "A simple handwoven rug that warms the bare floorboards. Finally, no more cold feet.",
    "oil_lantern": "A sturdy lantern for soft evening light. Hangs from the wall, casting gentle shadows.",
    "wooden_chair": "A creaky but comfortable chair by the window, perfect for watching the pond ripple.",
    "small_aquarium": "A tiny tank for displaying your favorite common catch. Bubbles softly in the corner.",
    "wall_shelf": "Shelves to display trinkets and rare drops. Clutter, but organized clutter.",
    "fishing_trophy_case": "A glass case for your proudest mounted fish.",
    "plush_armchair": "Sink into this overstuffed chair after a long day. Ideal for rainy-night dozing.",
    "glowing_plant_pot": "A pot with bioluminescent plants from glow scales. Emits a soft, ethereal light at night.",
    "large_aquarium": "A grand tank showcasing multiple rare fish. The centerpiece of any serious angler's shack.",
    "crystal_chandelier": "Crafted from lake shards; sparkles like the waters themselves. Pure ostentatious coziness.",
    "legendary_trophy_plaque": "A golden plaque for your Ghost Carp. The ultimate flex.",
    "riverside_landscape_painting": "A serene painting of the full watershed. Makes the shack feel vast and connected.",
}

decor_unlocks = {
    "cozy_rug": ["misty_creek"],  
    "oil_lantern": ["misty_creek"],
    "wooden_chair": ["misty_creek"],
    "small_aquarium": ["misty_creek"],
    "wall_shelf": ["shimmering_brook"],
    "fishing_trophy_case": ["shimmering_brook"],
    "plush_armchair": ["shimmering_brook"],
    "glowing_plant_pot": ["crystal_lake"],
    "large_aquarium": ["crystal_lake"],
    "crystal_chandelier": ["lake_master"], 
    "legendary_trophy_plaque": ["lake_guardian"],
    "riverside_landscape_painting": "logbook_100%" #custom check 
}

shop_prices = {
    "bait": {
        "insects": 80,
        "shimmerbait": 180,
        "glowworms": 500,
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
        "moonlight_guppy": 45,
        "deepwater_sturgeon": 90,
        "prism_trout": 160,
        "abyssal_angler": 100,
        "lunar_trout": 95,
        "ghost_carp": 800
    },

    "drops": {
        "wood_plank": 8,
        "iron_shard": 15, 
        "magical_resin": 50,
        "river_pearl": 65,
        "azure_fin": 60,
        "glow_scale": 35,
        "crystal_shard": 80,
        "moonstone": 120,
        "spectral_fin": 300
    },
    "decor": {
        "cozy_rug": 150,
        "oil_lantern": 250,
        "wooden_chair": 300,
        "small_aquarium": 450,
        "wall_shelf": 650,
        "fishing_trophy_case": 900,
        "plush_armchair": 900,
        "glowing_plant_pot": 1800,
        "large_aquarium": 2500,
        "crystal_chandelier": 3500,
        "legendary_trophy_plaque": 5000,
        "riverside_landscape_painting": 8000
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
    "Azure Gill": "azure_gill",
    "Moonlight Guppy": "moonlight_guppy",
    "Deepwater Sturgeon": "deepwater_sturgeon", 
    "Prism Trout": "prism_trout",
    "Abyssal Angler": "abyssal_angler",
    "Lunar Trout": "lunar_trout",
    "Ghost Carp": "ghost_carp"
}



fish_displays = {v: k for k,v in fish_name_map.items()}


sleep_prints = {
    "Clear": {
        "night": "You drift off under a blanket of stars visible through the window. Crickets chirp softly outside as dreams of calm waters take hold...",
        "day": "A short nap in the quiet shack refreshes you. Sunlight warms the floorboards."
    },

    "Rainy": {
        "night": "Rain patters rhythmically on the roof like a soothing lullaby. A frog croaks lazily outside, harmonizing with the downpour as you sink into deep, restorative sleep...",
        "day": "The steady rain on the roof creates a cocoon of sound. You rest, listening to droplets dance overhead."
    },
    "Foggy": {
        "night": "Thick fog muffles the world outside. The shack feels like a hidden sanctuary as you slip into a dreamy, hushed slumber.",
        "day": "Mist presses against the windows, turning the shack into a soft gray haven. Your brief rest feels timeless."
    },
    "Stormy": {
        "night": "Thunder rumbles distantly as wind howls around the eaves. Strangely, the storm's fury makes the shack feel safer; you sleep heavily, exhausted but secure.",
        "day": "Lightning flickers through the clouds. You nap fitfully, awakened occasionally by thunder, but still refreshed."
    }
}

class Player:
    def __init__(self, name):
        self.name = name
        self.fishing_skill = 1
        self.luck = 1                                                                                                                  #revert 100
        self.gear = {"rod": "wooden_rod", "bait": "worm"}
        self.inventory = {"fish": {}, "coins": 100, "items": {}, "rods": {}, "baits": {"worm": 10}}
        self.zone = 0
        self.dex = {}
        self.shack = {"unlocked": False, "decor": []}

def shop(player):
    shop_flavor = {
    0: {  # Beginner's Pond - Tackle Chest
        "welcome": f'"Hey there, {player.name}! Fresh bait just came in - take a look!"',
        "no_money": '"Tight on coins, eh? The pond\'s full of fish waiting to be caught!"',
        "thanks": '"There ya go! Those fish won\'t know what hit \'em!"',
        "closed": "The Tackle Chest is closed during night hours. Come back tomorrow.",
        "exit": f'"Come back soon, {player.name}! Don\'t let those fish get too comfortable!"',
        "invalid": '"Huh? You\'ll have to speak clearer, friend!"',
        "invalid_bait": '"That\'s not how we count bait around here, mate!"',
        "invalid_fish": '"That doesn\'t make sense..."',
        "invalid_item": '"Now what kind of item number is that?"',
        "cancel_bait": '"Changed your mind? No worries, take your time!"',
        "cancel_fish": '"No sale? The fish\'ll still be there tomorrow!"',
        "cancel_item": '"Keeping your treasures? Can\'t blame ya!"',
        "no_fish": '"No fish to sell? The pond\'s right there, mate!"',
        "no_items": '"Nothing to sell? Keep fishing - you\'ll find something!"'
    },
    1: {  # Misty Creek - Rusty Hook
        "welcome": '"What d\'ya need? I don\'t got all day for chit-chat."',
        "no_money": '"No coin, no bait. Simple as that."',
        "thanks": '"There. Now quit loitering."',
        "closed": "The Rusty Hook is shut tight. A sign says 'Closed - Gone Fishin'.",
        "exit": '"Don\'t bother me unless you\'re buying."',
        "invalid": '"Speak up or get out."',
        "invalid_bait": '"Numbers. Use \'em."',
        "invalid_fish": '"You counting fish that don\'t exist?"',
        "invalid_item": '"That ain\'t a real item."',
        "cancel_bait": '"Wasting my time. Typical."',
        "cancel_fish": '"Make up your mind next time."',
        "cancel_item": '"Can\'t decide? Figures."',
        "no_fish": '"No fish? What are you even doing here?"',
        "no_items": '"Empty pockets? Come back when you\'ve got something."'
    },
    2: {  # Shimmering Brook - Silver Scale
        "welcome": '"Welcome, discerning angler. Our selection is... curated for those with particular tastes."',
        "no_money": '"I\'m afraid our standards are rather exclusive. Perhaps when your means improve."',
        "thanks": '"An excellent choice. May it bring you fortune on the waters."',
        "closed": "The Silver Scale is closed. Through the window, you see elegant displays being covered for the night.",
        "exit": '"Do return when you require the finest angling supplies."',
        "invalid": '"I beg your pardon? Could you clarify?"',
        "invalid_bait": '"Our inventory is meticulously numbered. Please use the system."',
        "invalid_fish": '"I believe you\'ve misread our catalog."',
        "invalid_item": '"That selection doesn\'t appear in our registry."',
        "cancel_bait": '"A prudent reconsideration. Quality over haste."',
        "cancel_fish": '"Perhaps another time, when you\'re more certain."',
        "cancel_item": '"Discretion is the better part of commerce."',
        "no_fish": '"No specimens to offer? The brook awaits your skilled hand."',
        "no_items": '"No materials for trade? The waters hold many secrets yet."'
    },
    3: {  # Crystal Lake - Crystal Market
        "welcome": '"The waters call to you... as they call to all who seek what lies beneath."',
        "no_money": '"The lake\'s treasures require sacrifice. Return when you are prepared."',
        "thanks": '"May the crystal waters guide your line to wonders unseen."',
        "closed": "The Crystal Market vanishes into the mist at night, as if it were never there.",
        "exit": '"The lake holds many secrets... and so do I."',
        "invalid": '"The currents of meaning are unclear... speak plainly."',
        "invalid_bait": '"The numbers dance, but not in that pattern."',
        "invalid_fish": '"That quantity echoes in empty waters."',
        "invalid_item": '"That choice ripples without substance."',
        "cancel_bait": '"The bait returns to the depths, waiting."',
        "cancel_fish": '"The fish swim free for another day."',
        "cancel_item": '"Some treasures are meant to be kept."',
        "no_fish": '"The lake gives nothing to idle hands. Cast your line deeper."',
        "no_items": '"The crystals remain silent. You have nothing they desire."'
    }
}
    
    if time_of_day == "night":
        tprint(shop_flavor[player.zone]['closed'], 0.02)
        return
    tprint(shop_flavor[player.zone]['welcome'])

    shop_names = {
        0: "Tackle Chest",
        1: "Rusty Hook",
        2: "Silver Scale",
        3: "Crystal Market"
        }
    while True:

        

        

        print(f"Money: ${player.inventory['coins']}")
        print(f"=== The {shop_names[player.zone]} ===")
        print("=" * 40)
        stprint("  [1] --- Buy Bait")
        stprint("  [2] --- Sell Fish")
        stprint("  [3] --- Sell Items")
        stprint("  [4] --- Buy Home Decor")
        stprint("  [0] --- Exit Shop")

        main_selection = input("> ")
        if main_selection == "1":

            bait_options = {
                "1": "insects",
                "2": "shimmerbait",
                "3": "glowworms",
                "4": "golden_grubs"
            }

            tprint(shop_flavor[player.zone]['welcome'])
            
            stprint(f"[1] --- Insects")
            stprint(f"[2] --- Shimmerbait")
            stprint(f"[3] --- Glow Worms")
            stprint(f"[4] --- Golden Grubs")
            stprint(f"[0] --- Back")
            

            bait_selection = input("> ")
            if bait_selection not in ["1", "2", "3", "4", "0"]:
                tprint(shop_flavor[player.zone]['invalid_bait'])
                continue

            if bait_selection == "0":
                continue


            selected_bait = bait_options[bait_selection]
            selected_price = shop_prices["bait"][selected_bait]

            if player.inventory["coins"] < selected_price:
                tprint(shop_flavor[player.zone]['no_money'])
                continue

            tprint(f"{display_names['baits'][selected_bait].capitalize()}: costs ${selected_price}. Purchase? (y/n)", 0.01)
            confirm = input("> ")
            if confirm.lower() == "y":
                player.inventory["coins"] -= selected_price
                player.inventory["baits"][selected_bait] = player.inventory["baits"].get(selected_bait, 0) + 20
                print(f"Spent ${selected_price} on {display_names['baits'][selected_bait]}. Use [baits] outside of shop to equip.")
                tprint(shop_flavor[player.zone]['thanks'])
                continue
            else:
                tprint(shop_flavor[player.zone]['cancel_bait'])
                continue
            
            
            
        elif main_selection == "2":
            
            fish_inventory = player.inventory["fish"]

            if not fish_inventory: 
                tprint(shop_flavor[player.zone]['no_fish'])
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
                tprint(shop_flavor[player.zone]['invalid_fish'])
                continue
            elif int(fish_selection) < 1 or int(fish_selection) > len(fish_list):
                tprint(shop_flavor[player.zone]['invalid_fish'])
                continue


            selected_fish = fish_list[int(fish_selection) - 1]
            fish_external = fish_displays[selected_fish]

            print(f"{fish_external}: How many would you like to sell?")
            quantity = input("> ")
            if not quantity.isdigit(): 
                tprint(shop_flavor[player.zone]['invalid_fish'])
                continue
            quantity = int(quantity)
            if quantity > player.inventory['fish'][selected_fish]:
                tprint(shop_flavor[player.zone]['invalid_fish'])
                continue
            if quantity == 0:
                tprint(shop_flavor[player.zone]['cancel_fish'])
                continue

            price_fetched = shop_prices["fish"][selected_fish] * quantity

            player.inventory["fish"][selected_fish] -= quantity
            if player.inventory["fish"][selected_fish] == 0:
                del player.inventory["fish"][selected_fish]
            player.inventory["coins"] += price_fetched

            print(f"Sold {fish_external} x{quantity} for ${price_fetched}.")
            tprint(shop_flavor[player.zone]['thanks'])
            continue
        
        if main_selection == "3":

            
            drop_inventory = player.inventory["items"]

            if not drop_inventory: 
                tprint(shop_flavor[player.zone]['no_items'])
                input("> ")
                continue
            
            drop_list = list(drop_inventory.keys())

            for i, (drop_id, quantity) in enumerate(drop_inventory.items(), 1):
                drop_name = display_names['drops'].get(drop_id, drop_id)
                print(f"[{i}] --- {drop_name} (x{quantity})")
                time.sleep(0.04)
            print("[0] --- Back")


            drop_selection = input("> ")

            if drop_selection == "0":
                continue
            
            elif not drop_selection.isdigit():
                tprint(shop_flavor[player.zone]['invalid_item'])
                continue
            elif int(drop_selection) < 1 or int(drop_selection) > len(drop_list):
                tprint(shop_flavor[player.zone]['invalid_item'])
                continue


            selected_item = drop_list[int(drop_selection) - 1]
            drop_external = display_names['drops'][selected_item]

            print(f"{drop_external}: How many would you like to sell?")
            quantity = input("> ")
            if not quantity.isdigit(): 
                tprint(shop_flavor[player.zone]['invalid_item'])
                continue
            quantity = int(quantity)
            if quantity > player.inventory['items'][selected_item]:
                tprint(shop_flavor[player.zone]['invalid_item'])
                continue
            if quantity == 0:
                tprint(shop_flavor[player.zone]['cancel_item'])
                continue

            price_fetched = shop_prices["drops"][selected_item] * quantity

            player.inventory["items"][selected_item] -= quantity
            if player.inventory["items"][selected_item] == 0:
                del player.inventory["items"][selected_item]
            player.inventory["coins"] += price_fetched

            print(f"Sold {drop_external} x{quantity} for ${price_fetched}.")
            tprint(shop_flavor[player.zone]['thanks'])
            continue
        
        elif main_selection == "4":
            available_decor = [] #ones unlocked, either by zone or quest
            if quests["the_shack"]["status"] in ["active", "hidden"]:
                tprint("Nothing here just yet... explore more waters!")
                input("<press enter to return> ")
                continue

            for item, price in shop_prices["decor"].items():
                unlock_req = decor_unlocks.get(item, [])
                if isinstance(unlock_req, list):
                    checked = True
                    for req in unlock_req:
                        if req in zones:
                            if not zones[req]: 
                                checked = False
                                break
                        elif req in quests:
                            if not quests[req]["status"] == "complete":
                                checked = False
                                break
                    if checked:
                        available_decor.append((item, price))
                elif unlock_req == "logbook_100%":  
                    if logbook_completion(player):
                        available_decor.append((item, price))

            while True:
                for i, (item,price) in enumerate(available_decor, 1):
                    display_name = display_names["decor"][item]
                    owned_mark = "[OWNED]" if item in player.shack["decor"] else f"${price}" #show price if not owned
                    stprint(f"[{i}] {owned_mark} --- {display_name}")
                stprint("[0] --- Back")
                stprint("\nMore furnishings will unlock as you master new waters...")

                decor_selection = input("> ")

                if not decor_selection.isdigit():
                    tprint(shop_flavor[player.zone]["invalid"])
                    continue
                decor_selection = int(decor_selection)
                if decor_selection > len(shop_prices["decor"].keys()) or decor_selection < 0:
                    tprint(shop_flavor[player.zone]["invalid"])
                    continue
                
                if decor_selection == 0:
                    break
                    

                decor_list = list(shop_prices["decor"].keys())

                selected_decor = decor_list[decor_selection - 1] #-1 because user input is on 1-index while decor_list is zero-indexed
                display_name = display_names["decor"][selected_decor]
                desc = decor_descs[selected_decor]
                price = shop_prices["decor"][selected_decor]
                stprint(f"\n --- {display_name} ---")
                if selected_decor in player.shack["decor"]:
                    stprint(f"Owned. (${price})")
                    stprint(desc)
                    stprint("\n<press enter to return>")
                    input("> ")
                    continue
                    
                else: 
                    stprint(f"--- ${price} {display_name}")
                    stprint(f"\n {desc}\n")
                    if player.inventory["coins"] >= price:
                        print("You can afford this item.")
                        print("Purchase? (y/n)")
                        confirm = input("> ")
                        if confirm.lower() == "y":
                            player.inventory["coins"] -= price
                            player.shack["decor"].append(selected_decor)
                            time.sleep(1)
                            tprint(f"You purchased the {display_name}! Added to your home.")
                    tprint("<press enter to continue>")
                    input("> ")
                    continue

                
            



        else: 
            tprint(shop_flavor[player.zone]['exit'])
            return
        
def logbook_completion(player):
    if len(player.dex.keys()) >= len(fish_classes.keys()):
        return True
    return False

def workshop(player):

    workshop_flavor = {
    0: {  # Beginner's Pond - Grumpy Old Craftsman
        "welcome": '"*grunt* What do you want? Can\'t you see I\'m busy?"',
        "day_closed": '"Workshop\'s closed! Come back when the moon\'s out."',
        "exit": '"About time. Don\'t track mud on your way out."',
        "invalid": '"Eh? Speak proper or don\'t speak at all."',
        "no_recipes": '"Nothing for greenhorns like you. Come back when you\'ve actually caught something."',
        "no_quests": '"No handouts here. Earn your keep first."',
        f"craft_success": '"There. A new rod. Try not to break it like the last one."',
        "craft_fail": '"You call that a proper offering? Come back with real materials."',
        "craft_cancel": '"Wasting my time. Should\'ve known."',
        f"bait_success": '"There, special bait. Don\'t expect miracles."',
        "bait_fail": '"Not enough. My workshop isn\'t a charity."',
        "quest_complete": '"*mumbles* Not completely useless, I suppose."',
        "quest_view": '"These are the tasks. Take \'em or leave \'em."',
        "working": '"*hammering noises* Can\'t you see I\'m working here?"'
    },
    1: {  # Misty Creek - Eccentric Inventor
        "welcome": '"Aha! A test subject! I mean... customer! What marvelous contraption can I build for you today?"',
        "day_closed": '"The workshop is... undergoing... recalibration! Yes! Come back tonight!"',
        "exit": '"Farewell! Tell the fish I\'m working on something... spectacular!"',
        "invalid": '"That input doesn\'t compute with my magnificent brain!"',
        "no_recipes": '"My genius requires more... exotic materials! Bring me creek treasures!"',
        "no_quests": '"No experiments running at the moment! Science must wait!"',
        f"craft_success": '"BEHOLD!! My greatest invention yet! Probably!"',
        "craft_fail": '"The quantum flux capacitors are misaligned! More materials required!"',
        "craft_cancel": '"Aborting the creative process! The tragedy! The humanity!"',
        f"bait_success": '"Bait!!! It might attract fish! Or aliens! Science will tell!"',
        "bait_fail": '"Insufficient anomalous particles! The creek hides more secrets!"',
        "quest_complete": '"DATA COLLECTED! Hypothesis: You\'re actually competent!"',
        "quest_view": '"Observe my brilliant field tests! I mean... quests!"',
        "working": '"EUREKA! No, wait, false alarm. Carry on."'
    },
    2: {  # Shimmering Brook - Mystical Artisan
        "welcome": '"The silver threads of fate have drawn you here. What creation calls to your imagination?"',
        "day_closed": '"The workshop slumbers while sunlight dances on the water. Return when shadows lengthen."',
        "exit": '"Go with the current\'s blessing. May your line find what your heart seeks."',
        "invalid": '"Your words scatter like leaves on the water. Choose with intention."',
        "no_recipes": '"The brook has not yet whispered the patterns you seek. Patience, child of the water."',
        "no_quests": '"The flowing ones have set no trials for you. Your path unfolds differently."',
        f"craft_success": '"From water\'s memory and starlight\'s touch... May it serve your journey well."',
        "craft_fail": '"The elements do not align. The brook asks for more of its essence."',
        "craft_cancel": '"Some creations must wait for their proper moment. You are wise to listen."',
        f"bait_success": '"Here is your bait. It carries the brook\'s own song. Use it with respect."',
        "bait_fail": '"The balance of elements is incomplete. The silver waters offer more to those who listen."',
        "quest_complete": '"The flowing ones are pleased. You honor the ancient pact between angler and water."',
        "quest_view": '"These are the tasks the water has woven into your path. Each completes a pattern in the great flow."',
        "working": '"*humming* The water sings through my hands... the patterns emerge..."'
    },
    3: {  # Crystal Lake - Practical Mountaineer
        "welcome": '"Took you long enough to find this place. I don\'t work with amateurs - show me what you\'ve got."',
        "day_closed": '"Workshop\'s closed. I\'m out surveying the lake. Come back after dark."',
        "exit": '"Watch your step on the way down. These cliffs don\'t forgive mistakes."',
        "invalid": '"Speak clearly. The thin air getting to you already?"',
        "no_recipes": '"You\'re not ready for high-altitude gear. Come back when you\'ve braved the deeper waters."',
        "no_quests": '"No tasks for you. The lake tests everyone in its own way."',
        f"craft_success": '"There. Built to handle pressure you can\'t even imagine."',
        "craft_fail": '"Not enough quality materials. The lake doesn\'t give up its treasures easily."',
        "craft_cancel": '"Smart. High-altitude gear isn\'t for the uncertain."',
        f"bait_success": '"Fancy bait. Works better when your hands aren\'t shaking from the cold."',
        "bait_fail": '"You\'re short on materials. The crystal deposits are deeper than you think."',
        "quest_complete": '"You handled that better than most. Maybe you\'ve got what it takes for these waters."',
        "quest_view": '"These are the jobs that need doing up here. Take your pick if you think you can handle it."',
        "working": '"*sharpening tools* High-altitude maintenance. Never ends."'
    }
}

    if time_of_day == "day":
        tprint(workshop_flavor[player.zone]["day_closed"])
        return

    tprint(workshop_flavor[player.zone]["welcome"])
    while True:
        print("=== Workshop ===")
        print("=" * 40)
        
        
        
        stprint("[1] --- Crafting")
        stprint("[2] --- Quests")
        stprint("[0] --- Leave")

        main_select = input("> ")

        if main_select not in ["1", "2", "0"]: 
            tprint(workshop_flavor[player.zone]["invalid"])
            continue
        if main_select == "0":
            tprint(workshop_flavor[player.zone]["exit"])
            return

        if main_select == "1":
            print("=== Crafting ===")
            stprint("[1] --- Rods")
            stprint("[2] --- Baits")  
            stprint("[0] --- Back\n")
            selection = input("> ")
            if selection not in ["1", "2", "0"]:
                tprint(workshop_flavor[player.zone]["invalid"])
                continue

            if selection == "0":
                tprint(workshop_flavor[player.zone]["working"])
                continue

            if selection == "1":
                available_recipes = []
                for recipe_id, recipe_data in crafting_recipes.items():
                    if zones[recipe_data["unlock_zone"]] and recipe_data["type"] == "rod":
                        available_recipes.append((recipe_id, recipe_data))
                
                if not available_recipes:
                    tprint(workshop_flavor[player.zone]["no_recipes"])
                    continue
                
                for i, (recipe_id, recipe_data) in enumerate(available_recipes, 1):
                    stprint(f"[{i}] --- {recipe_data['name']}")
                
                stprint("[0] --- Back")
                
                craft_select = input("> ")
                if craft_select == "0":
                    continue
                
                if not craft_select.isdigit():
                    tprint(workshop_flavor[player.zone]["invalid"])
                    continue
                if int(craft_select) < 1 or int(craft_select) > len(available_recipes):
                    tprint(workshop_flavor[player.zone]["working"])
                    continue
                
                selected_recipe_id, selected_recipe = available_recipes[int(craft_select) - 1]
                
                tprint(f"-- {selected_recipe['name']} --")
                time.sleep(0.05)
                stprint(f"Description: {selected_recipe['description']}")
                stprint(f"Requirements:")
                
                can_craft = True
                for requirement, quantity in selected_recipe["requirements"].items():
                    display_name = display_names['drops'].get(requirement) or fish_displays.get(requirement)
                    
                    if requirement in player.inventory['items']:
                        current = player.inventory['items'].get(requirement, 0)
                    elif requirement in player.inventory['fish']:
                        current = player.inventory['fish'].get(requirement, 0)
                    else:
                        current = 0
                        
                    status = "✓" if current >= quantity else "✗"
                    stprint(f" {status} {display_name}: {current}/{quantity}")
                    if current < quantity:
                        can_craft = False
                
                stprint(f" {('✓' if player.inventory['coins'] >= selected_recipe['cost'] else '✗')} Coins: ${player.inventory['coins']}/${selected_recipe['cost']}")
                if player.inventory['coins'] < selected_recipe['cost']:
                    can_craft = False
                
                stprint("Craft? (y/n)")
                confirm = input("> ")
                
                if confirm.lower() == "y":
                    if can_craft:
                        for req, quantity in selected_recipe["requirements"].items():
                            if req in player.inventory["items"]:
                                player.inventory["items"][req] -= quantity #checks if drop or fish
                                if player.inventory["items"][req] == 0:
                                    del player.inventory["items"][req]
                            elif req in player.inventory["fish"]: #if fish
                                player.inventory["fish"][req] -= quantity
                                if player.inventory["fish"][req] == 0:
                                    del player.inventory["fish"][req]
                        
                        player.inventory["coins"] -= selected_recipe["cost"]
                        
                        player.inventory["rods"][selected_recipe_id] = player.inventory["rods"].get(selected_recipe_id, 0) + 1
                        
                        craft_time = random.randint(5, 10)
                        tprint(f'Crafting ... (Est. {craft_time} seconds...)', 0.03)
                        time.sleep(craft_time)
                        tprint("Completed!", 0.02)
                        tprint(workshop_flavor[player.zone]["craft_success"])
                    else:
                        tprint(workshop_flavor[player.zone]["craft_fail"])
                else:
                    tprint(workshop_flavor[player.zone]["craft_cancel"])



            elif selection == "2": #baits
                available_baits = []
                for recipe_id, recipe_data in crafting_recipes.items():
                    if zones[recipe_data["unlock_zone"]] and recipe_data["type"] == "bait":
                        available_baits.append((recipe_id, recipe_data))
            
                for i, (recipe_id, recipe_data) in enumerate(available_baits, 1):
                    stprint(f"[{i}] --- {recipe_data['name']} (x{recipe_data['quantity']})")
                
                stprint("[0] --- Back")
                
                craft_select = input("> ")
                if craft_select == "0":
                    continue
                
                if not craft_select.isdigit():
                    tprint(workshop_flavor[player.zone]['invalid'])
                    continue
                if int(craft_select) < 1 or int(craft_select) > len(available_baits):
                    tprint(workshop_flavor[player.zone]['working'])
                    continue
                
                selected_recipe_id, selected_recipe = available_baits[int(craft_select) - 1]
                
                tprint(f"-- {selected_recipe['name']} --")
                time.sleep(0.05)
                stprint(f"Description: {selected_recipe['description']}")
                stprint(f"Requirements:")
                
                can_craft = True
                
                for req, quantity in selected_recipe["requirements"].items():
                    display_name = display_names["drops"].get(req) or fish_displays.get(req)
                    if req in player.inventory['items']:
                        current = player.inventory['items'].get(req, 0)
                    elif req in player.inventory['fish']:
                        current = player.inventory['fish'].get(req, 0)
                    else:
                        current = 0

                    status = "✓" if current >= quantity else "✗"
                    stprint(f" {status} {display_name}: {current}/{quantity}")
                    if current < quantity:
                        can_craft = False
                
                stprint(f" {('✓' if player.inventory['coins'] >= selected_recipe['cost'] else '✗')} Coins: ${player.inventory['coins']}/${selected_recipe['cost']}")
                if player.inventory['coins'] < selected_recipe['cost']:
                    can_craft = False
                
                stprint("Craft? (y/n)")
                confirm = input("> ")
                
                if confirm.lower() == "y":
                    if can_craft:
                        for req, quantity in selected_recipe["requirements"].items():
                            if req in player.inventory["items"]: #checks if item or fish
                                player.inventory["items"][req] -= quantity
                                if player.inventory["items"][req] == 0:
                                    del player.inventory["items"][req]
                            elif req in player.inventory["fish"]:
                                player.inventory["fish"][req] -= quantity
                                if player.inventory["fish"][req] == 0:
                                    del player.inventory['fish'][req]
                        
                        player.inventory["coins"] -= selected_recipe["cost"]
                        
                        bait_id = selected_recipe.get("crafted_item", selected_recipe_id)
                        player.inventory["baits"][bait_id] = player.inventory["baits"].get(bait_id, 0) + selected_recipe["quantity"]
                        
                        craft_time = random.randint(3, 6) 
                        tprint(f'Crafting bait... (Est. {craft_time} seconds...)', 0.03)
                        time.sleep(craft_time)
                        tprint("Completed!", 0.02)
                        tprint(workshop_flavor[player.zone]['bait_success'])
                    else:
                        tprint(workshop_flavor[player.zone]['bait_fail'])
                else:
                    tprint(workshop_flavor[player.zone]['working'])
                    

        if main_select == "2":
            print("=== Quests ===")
            active_quests = []
            complete_quests = []
            unlocked_quests_list = []

            for quest_id, quest_data in quests.items():
                if quest_data["status"] == "active": 
                    active_quests.append(quest_id)
                elif quest_data["status"] == "complete":
                    complete_quests.append(quest_id)

            unlocked_quests_list = active_quests + complete_quests

            print("\n\n --- Active ---")
            for i, quest_id in enumerate(active_quests, 1):
                stprint(f"[{i}] --- {quests[quest_id]['name']}")

            print("\n--- Completed ---")
            for i, quest_id in enumerate(complete_quests, len(active_quests) + 1):
                stprint(f"[{i}] --- {quests[quest_id]['name']}")
            print("[0] --- Back")

            selection = input("> ")
            
            if not selection.isdigit():
                tprint(workshop_flavor[player.zone]["invalid"])
                continue
            
            selection = int(selection)
            if selection == 0:
                continue
            
            if selection < 1 or selection > len(unlocked_quests_list):
                tprint(workshop_flavor[player.zone]["invalid"])
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
                tprint(workshop_flavor[player.zone]["quest_view"])
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
                    elif requirement in fish_displays:
                        current = player.inventory['fish'].get(requirement, 0)
                        stprint(f" - {fish_displays[requirement]} | {current}/{needed}")
                        if current >= needed: 
                            completed_reqs += 1
                
                if total_reqs == completed_reqs:
                    # confirm + complete!
                    tprint("You've fulfilled all the requirements! Finish Quest? (y/n) ")
                    confirm = input("> ")
                    if confirm.lower() == "y":
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
                        
                        for reward, spec in selected_quest_data['rewards'].items():
                            if reward in zones:
                                zones[reward] = True
                            elif reward == "skill": 
                                player.fishing_skill += spec
                            elif reward == "luck":
                                player.luck += spec
                            elif reward == "money":
                                player.inventory["coins"] += spec
                            elif reward == "shack":
                                player.shack["unlocked"] = True
                        
                        print("\n==============================")
                        stprint(f" QUEST COMPLETE: {selected_quest_data['name'].upper()} ")
                        print("==============================\n")
                        stprint(f"{selected_quest_data['complete_description']}\n")
                        stprint("Rewards:")
                        for reward, spec in selected_quest_data["rewards"].items():
                            if reward == "skill":
                                stprint(f" - +{spec} Fishing Skill")
                            elif reward == "luck":
                                stprint(f" - +{spec} Base Fishing Luck")
                            elif reward == "money": 
                                stprint(f" - +{spec} coins!")
                            elif reward in zones:
                                stprint(f" - {display_names['zones'][reward]} unlocked!")
                            elif reward == "shack":
                                stprint(f" - Unlocked the [home] command + [setlines] command")
                        
                        selected_quest_data['status'] = "complete"
                    
                        stprint("\n==============================\n")
                        tprint(workshop_flavor[player.zone]['quest_complete'], 0.008)
                        
                        input("(press <enter> to continue)")
                    else:
                        continue

                
            
                

            

def inventory(player):
    stprint(f"\n-- {player.name}'s Inventory -- \n")
    
    print(f"Money: ${player.inventory['coins']}\n")

    print("Equipped Gear:")
    rod_code = player.gear["rod"]
    bait_code = player.gear["bait"]
    luck_marker = f"(+{rods[rod_code][1]} luck)" if rods[rod_code][1] > 1 else ""
    
    stprint(f"Rod: {display_names['rods'][rod_code]} (+{rods[rod_code][0]} skill) {luck_marker}")
    stprint(f"Bait: {display_names['baits'][bait_code]} (+{baits[bait_code]} skill, +{bait_luck[bait_code]}% luck)\n")
    
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



def shack(player):
    if player.shack['unlocked'] == False:
        tprint("The shack remains locked...")
        return

    tprint("You enter your little cabin; a wooden sign hangs above the doorway, your name hand-carved onto it.")
    if player.shack["decor"]:
        tprint("Your shack is adorned with: " + ", ".join([display_names["decor"].get(decor, decor) for decor in player.shack["decor"]]) + ".")
        tprint("It brings a touch of warmth to the humble space.")  
    else:
        tprint("The shack feels bare - perhaps some furnishings from the shop would help?")
    shack_int(player)
    return


def shack_int(player):
    while True:
        print(f"\n=== {player.name}'s Shack ===")
        stprint("[1] --- Rest/Sleep")
        stprint("[2] --- View Journal (Stats)")
        stprint("[0] --- Exit Shack")

        command = input(">")
        match command:
            case "exit" | "leave" | "return" | "0": 
                tprint("You exit the cabin.")
                break
            case "sleep" | "rest" | "1":
                sleep_shack(player)
                continue
            case "2" | "journal" | "stats":
                view_journal(player)
                continue
            case _:
                stprint("That's not a valid command.")
                continue
        
    return


def view_journal(player): 
    tprint("You open your weathered journal...")
    time.sleep(0.5)
    print("\n" + "="*40)
    stprint(f"  {player.name}'s Fishing Records")

    #base stats
    stprint("\n--- Fisher Profile ---")
    stprint(f"Fishing Skill: {player.fishing_skill}")
    stprint(f"Natural Luck: {player.luck}")

    #gears, luck &skill
    rod = player.gear["rod"]
    bait = player.gear["bait"]
    rod_skill, rod_luck = rods[rod]
    bait_skill = baits[bait]
    bait_luck_buff = bait_luck[bait] #my bad code - bait skill and luck should've been kept together like in rods, but my bait luck was added later. -_buff to prevent name overlap.

    stprint(f"\n--- Current Equipment ---")
    stprint(f"Rod: {display_names['rods'][rod]}")
    stprint(f"--   +{rod_skill} skill, +{rod_luck} luck")
    stprint(f"Bait: {display_names['baits'][bait]}")
    stprint(f"--   +{bait_skill} skill, +{bait_luck_buff} luck")

    total_skill = player.skill + rod_skill + bait_skill
    total_luck = player.luck + bait_luck_buff + rod_luck

    stprint(f"\n--- Effective Totals ---")
    stprint(f"Total Fishing Skill: {total_skill}")
    stprint(f"Total Luck: {total_luck:.2f}")

    #fish
    stprint(f"\n--- Discoveries ---")
    total_fish = len(fish_classes.keys())
    discovered_fish = len(player.dex.keys())
    stprint(f"Fish Species: {discovered_fish}/{total_fish} ({discovered_fish/total_fish*100:.0f}%)")
    stprint(f"Total Catches: {sum(player.dex.values())}")
            
    top_fish = max(player.dex.items(), key=lambda x: x[1]) #fancy lambda, to return both the name and the value
    fish_name = fish_displays[top_fish[0]]
    stprint(f"Most Caught: {fish_name} ({top_fish[1]} times)")

    stprint(f"\n--- Waters Explored ---")
    for zone_code, unlocked in zones.items():
        if unlocked:
            zone_name = display_names['zones'][zone_code]
            zone_fish = 0 #this is a number cause we're not taking a list of names - we only need the number of fish found.
            zone_discovered = 0
            for fish_id, fish_class in fish_classes.items():
                fish_instance = fish_class()
                zone_index = list(zones.keys()).index(zone_code) #zone code is internal name
                if zone_index in fish_instance.zones: 
                    zone_fish += 1
                    if fish_id in player.dex:
                        zone_discovered += 1
            
            if zone_fish > 0:
                percent = (zone_discovered/zone_fish)*100
                stprint(f"{zone_name}: {zone_discovered}/{zone_fish} ({percent:.0f}%)")
    
    print("\n" + "="*40)
    tprint("Press <enter> to close journal...")
    input("> ")
    


def sleep_shack(player):
    global turn, time_of_day

    tprint(sleep_prints[current_weather][time_of_day])
    if time_of_day == "day": 
        turn += 3
        time.sleep(1)
        manage_time()

        return
    else:
        full_cycle = PERIOD_LENGTH * 2
        #push to new morning
        turn = ((turn // full_cycle) + 1) * full_cycle
        time.sleep(1.5)

        manage_time()
    return




def logbook(player):
    while True:
        stprint("\n ===== Logbook ===== \n")
        print("=" * 45)
        found_fish = []
        shown_fish = []
        unlocked_zones = []
        unq_counter = 0
        unq_found_counter = 0
        
        for zone_code, state in zones.items():
            if state == True:
                unlocked_zones.append(zone_code)

        for fish_id, fish_class in fish_classes.items():
            fish_instance = fish_class()
            for zone_index in fish_instance.zones:
                zone_codes = list(zones.keys())
                if zone_index < len(zone_codes) and zones[zone_codes[zone_index]]:
                    if fish_id not in shown_fish:
                        shown_fish.append(fish_id)
                        unq_counter += 1
                        
                        if player.dex.get(fish_id, 0) > 0: unq_found_counter +=1
        

        stprint(f"Discovered in visible waters: {unq_found_counter} out of {unq_counter} unique species ({int(unq_found_counter/unq_counter * 100)}%)")
        stprint(f"Discovered out of whole world: {unq_found_counter} out of {len(fish_classes.keys())} ({int(unq_found_counter/len(fish_classes.keys()) * 100)}%)")
        for i, fish_internal in enumerate(shown_fish, 1):
            fish_external = fish_displays[fish_internal]
            printed = f"{fish_external}" if player.dex.get(fish_internal, 0) > 0 else "? ???"
            stprint(f"[{i}] {printed}")
            if printed != "? ???":
                found_fish.append(fish_internal)
        stprint("[0] --- Cancel")

        selection = input("> ")
        if not selection.isdigit():
            print("That's not an option... "); continue
            
        selection = int(selection)
        if selection > len(shown_fish) or selection < 0: 
            print("That's not an option... "); continue
        
        if selection == 0:
            print("Exiting Logbook...")
            return
        
        selected_fish = shown_fish[selection - 1]  
        if selected_fish not in found_fish:
            print("??? You haven't discovered this fish yet!")
        else:
            fish_external = fish_displays[selected_fish]
            fish_internal = selected_fish
            instance = fish_classes[selected_fish]()
            difficulty = instance.difficulty
            zone_names = []
            for zone_index in instance.zones:
                zone_codes = list(zones.keys())
                if zone_index < len(zone_codes):
                    zone_names.append(display_names['zones'][zone_codes[zone_index]])
            
            stprint(f"-- {fish_external} -- ")
            tprint(f"{fish_descriptions[fish_internal]}")
            stprint(f"Caught {player.dex.get(selected_fish, 0)} times.")  
            stprint(f"Found in {', '.join(zone_names)}.")
            stprint(f"{instance.day_rarity.lower()} during the day; {instance.night_rarity.lower()} at night.")
            stprint(f"Strength: {difficulty}")
            if hasattr(instance, "drops"):
                drop_list = [f"{display_names['drops'].get(drop, drop)} ({chance*100:.0f}%)" 
                            for drop, chance in instance.drops.items()]
                stprint(f"Drops: {', '.join(drop_list)}")
            stprint("Press <enter> to return...")
            if input("> ") == "":
                continue
            else: print("Exiting Logbook:"); return


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

    if (player.dex.get("crystal_koi", 0) > 0 and quests["crystal_lake_expedition"]["status"] == "hidden"):
        unlock_quest("crystal_lake_expedition")
    
    if zones["misty_creek"] and quests["pond_master"]["status"] == "hidden":
        unlock_quest("pond_master")
    if zones["shimmering_brook"] and quests["creek_master"]["status"] == "hidden":
        unlock_quest("creek_master")
        
    if zones["crystal_lake"] and quests["brook_master"]["status"] == "hidden":
        unlock_quest("brook_master")
        
    if zones["crystal_lake"] and quests["lake_master"]["status"] == "hidden":
        unlock_quest("lake_master")

    if quests["lake_master"]["status"] == "complete" and quests["lake_guardian"]["status"] == "hidden":
        unlock_quest("lake_guardian")
    
    if quests["pond_master"]["status"] == 'complete' and quests["the_shack"]["status"] == "hidden": 
        unlock_quest("the_shack")
    
    



def switch_zone(player):
    print("\n--- Unlocked Fishing Zones ---\n")
    unlocked_list = []
    for i, (zone_code, status) in enumerate(zones.items(), 1):
        if status:
            current_marker = "[CURRENT ZONE]" if i - 1 == player.zone else ""
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
    
    
#print then wait
def stprint(line, delay=0.07):
    print(line)
    time.sleep(delay)
    


def spawn_fish(player_zone, time_of_day):
    possible_fish = [] #possible fish - in this zone
    
    current_bait = player.gear["bait"]
    if player.inventory["baits"][current_bait] < 1:
        tprint(f"You're out of {display_names['baits'][current_bait]}! Visit The Tackle Shop to buy more or switch using [baits].")
        return
    player.inventory["baits"][current_bait] -= 1
    

    
    if not setting_lines: 
        tprint(f"You flick the rod, and the line arcs over the water...", 0.007)
        time.sleep(random.uniform(1, 5))

    if time_of_day == "night" and current_bait == "lunar_lure": #checks for the lunar lure - only allows nocturnal and glow to be caught
        for fish_name, fish_class in fish_classes.items():
            fish_instance = fish_class()
            if player_zone in fish_instance.zones and ("glow" in fish_instance.traits() or "nocturnal" in fish_instance.traits()):
                possible_fish.append(fish_instance)
    else:
        for fish_name, fish_class in fish_classes.items(): #normal spawn
            fish_instance = fish_class()
            if player_zone in fish_instance.zones:
                if time_of_day == "night" and fish_instance.night_rarity == "Not Found": continue
                elif time_of_day == "day" and fish_instance.day_rarity == "Not Found": continue
                possible_fish.append(fish_instance)
    
    if not possible_fish:
        return None
    
    
    current_rod = player.gear['rod']
    current_bait = player.gear['bait']
    effective_luck = player.luck + rods[current_rod][1] + bait_luck[current_bait]
    if setting_lines: effective_luck *= 0.5

    if current_weather == "Clear": effective_luck *= 1.15
    if current_weather == "Stormy": effective_luck *= 0.8

    og_roll = random.random() #original roll
    if random.random() < (effective_luck - 1): #runs a chance for second roll
        roll = min(og_roll, random.random()) #if so, roll again, pick best of two
    else: roll = og_roll #single roll
    
    if roll < 0.0008: rolled_type = "Legendary"
    elif roll < 0.0033: rolled_type = "Extremely Rare"
    elif roll < 0.0183: rolled_type = "Very Rare"
    elif roll < 0.0683: rolled_type = "Rare"
    elif roll < 0.2183: rolled_type = "Uncommon"
    else: rolled_type = "Common"

    fish_in_roll = [] #fish in this zone and rarity
    for fish_instance in possible_fish:
        if time_of_day == "day":
            if rolled_type == fish_instance.day_rarity:
                fish_in_roll.append(fish_instance)
        elif time_of_day == "night":
            if rolled_type == fish_instance.night_rarity:
                fish_in_roll.append(fish_instance)

    if len(fish_in_roll) == 0: rolled_type = None #if there are no fish in this rarity, catch seaweed

    if rolled_type == None:
        return None
    else: 
        fish_spawned = random.choice(fish_in_roll) 
        return fish_spawned

def manage_fish():
    global player
    fished = spawn_fish(player.zone, time_of_day)
    if fished == None: 
        print("Nothing but seaweed. Eugh.")
        return
    else: 
        rarity = fished.day_rarity if time_of_day == "day" else fished.night_rarity
        if not setting_lines:
            tprint(f"Tug - something's on the line! It's a {fished.name} ({rarity}) || Press <enter> to reel... ", 0.008)
            if rarity in ["Extremely Rare", "Legendary"]:
                stprint("\n")
                stprint("!!! " * 8)
                tprint(f"==== YOU'VE HOOKED A {rarity.upper()} FISH! ====")
                stprint("!!! " * 8)
            flush_input()
            input("> ")
        reeled = reel_fish(player, fished, time_of_day)
        if reeled:
            if hasattr(fished, "drops"):
                for item, rarity in fished.drops.items():
                    if random.random() <= rarity:
                        if not setting_lines:
                            print(f"The {fished.name} dropped 1 {display_names['drops'][item]}!")
                        player.inventory["items"][item] = player.inventory["items"].get(item, 0) + 1
                        #setlines
                        if setting_lines:
                            caught_while_setlines["drops"][item] = caught_while_setlines["drops"].get(item, 0) + 1

            internal_fished = fish_name_map[fished.name]
            player.dex[internal_fished] = player.dex.get(internal_fished, 0) + 1
            if player.dex[internal_fished] == 1: #your first catch
                print(f"Your first {fished.name} catch! Added to [logbook].") #NO need to check because no new catches allowed while setline
        


def reel_fish(player, fish, time_of_day,tick_duration=0.4):
    fish_internal_name = fish_name_map[fish.name]
    if fish_internal_name not in player.dex.keys() and setting_lines: #ONLY IF SETTING LINES, GIVE THE FISH FREEDOM IF NO DISCOVERED
        return False
    
    if random.randint(1, 100) <= fish.escape_chance(player.fishing_skill, time_of_day, player.gear["bait"]):
        if not setting_lines:
            print(f"Oop- the fish wriggles free!")
        return False
    
    success_texts = [
        f"Success! You've landed a {fish.name}!",
        f"Got it! The {fish.name} is yours.",
        "Victory! The fish is in your hands."
        ]
    
    fail_texts = [
        "Snap! Looks like you underestimated it.",
        "The line breaks! It's gone.",
        "The line snaps! Unlucky..."
    ]
    
    

    progress = 0
    bar_length = 20
    
    #base calc
    effective_skill = player.fishing_skill + rods[player.gear["rod"]][0] + baits[player.gear["bait"]]
    effective_difficulty = max(0.5, fish.difficulty * 0.8 - effective_skill * 0.6) 
    ticks = 20 + int(fish.difficulty * 1.2)  #longer total ticks/chances for harder fish
    progress_chance = min(0.90, 0.35 + (0.07 * effective_skill) - (0.02 * effective_difficulty)) 


    #weather calc
    if current_weather == "Foggy": effective_difficulty *= 1.15
    elif current_weather == "Stormy": effective_difficulty *= 1.2
    elif "Rainy" and "nocturnal" in fish.traits: effective_skill *= 1.25

    #lunar bait calc
    if time_of_day == "night" and player.gear['bait'] == "lunar_lure": effective_skill += 4

    for i in range(ticks):
        #we cap progress chance at 0.85.just to make it a little funner.
        progress_chance = min(0.85, 0.4 + (0.05 * effective_skill) - (0.03 * effective_difficulty))
        rng = random.random()
        if rng < progress_chance:
            progress = min(100, progress + random.randint(15,25))
        else: 
            progress = max(0, progress - random.randint(4, 8))
        filled = int(progress / 100 * bar_length)
        if random.random() < 0.1 and "jumpy" in fish.traits:
            progress = int(max(0, progress -  (progress * 0.20)))
            if not setting_lines:
                print("The fish thrashes! You lose 20% of progress!")

        bar = "█" * filled + "░" * (bar_length - filled)
        if not setting_lines:
            print(f"Reeling >>> [{bar}] {progress}%")

        if progress >= 100:
            if not setting_lines:
                print(random.choice(success_texts))
            internal = fish_name_map[fish.name]
            player.inventory["fish"][internal] = player.inventory["fish"].get(internal, 0) + 1
            caught_while_setlines["fish"][internal] = caught_while_setlines["fish"].get(internal, 0) + 1
            return True

        
        if not setting_lines:
            time.sleep(tick_duration)
        i += 1 

    if not setting_lines:
        print(random.choice(fail_texts))
    return False

def zone_info(player):
    zone_name = display_names['zones'][list(zones.keys())[player.zone]]
    stprint(f"\n--- {zone_name} ---")
    
    flavor_texts = {
        0: "Calm, shallow waters perfect for beginners.",
        1: "A flowing creek with deeper pools and faster currents.",
        2: "Crystal-clear brook where light dances on the surface.",
        3: "Deep, mysterious lake with secrets in its depths."
    }
    
    stprint(flavor_texts.get(player.zone, "???"))
    

    if time_of_day == "night":
        stprint("The darkness makes fishing challenging.")
    if current_weather == "Rainy":
        stprint("Rain patters on the water's surface.")

    current_zone_fish = []
    for fish_name, fish_class in fish_classes.items():
        fish_instance = fish_class()
        rarity = fish_instance.day_rarity if time_of_day == "day" else fish_instance.night_rarity
        if player.zone in fish_instance.zones:
            if rarity != "Not Found":
                current_zone_fish.append(fish_instance)
    
    if not current_zone_fish:
        print("No fish can be found at this time...")
        tprint("Press <enter> to continue...")
        input("> ")
        return
    stprint("Fish you've discovered here:")
    discovered_any = False
    for fish in current_zone_fish:
        fish_internal = fish_name_map[fish.name]
        if fish_internal in player.dex.keys():
            rarity = fish.day_rarity if time_of_day == "day" else fish.night_rarity
            stprint(f"{fish.name} - {rarity}")
            discovered_any = True
        else:
            stprint(f"??? - ???")
    
    if not discovered_any:
        stprint("You haven't discovered any fish here yet. Keep fishing!")
    
    print("Press <enter> to continue...")
    input("> ")

def setlines(quantity, player, time_of_day):
    global turn, setting_lines, caught_while_setlines
    
    caught_while_setlines = {
        "fish": {},
        "drops": {}
    }
    #VALID SETLINES CHECKS

    if not quantity.isdigit():
        print("Bad usage - quantity must be a number!")
        return
    quantity = int(quantity)
    if quantity > 200:
        print("Maximum lines set is 200.")
        return
    if quantity < 1:
        print("You must set a minimum of one line.")
        return
    current_bait = player.gear["bait"]
    current_bait_quantity = player.inventory["baits"].get(current_bait, 0) #CANNOT USE MORE THAN YOU HAVE IN BAIT, cannot set with worms. HARD CAP OF 200 SETLINES
    if quantity > current_bait_quantity:
        print(f"You can't set that many lines - you only have {current_bait_quantity} {current_bait}.")
        return
    if current_bait == "worm": 
        print("Worms dissolve too quickly to use in setlines. Try insects or better bait..")
        return
    

    setting_lines = True
    turns_used = math.ceil(quantity/10)
    for _ in range(quantity):
        spawn_fish(player.zone, time_of_day)
    tprint("You set your lines and wait awhile.")
    time.sleep(2)
    tprint(f"\nLines set, fish caught. {turns_used} hours have passed. Results:")
    stprint("\n-- Fish:\n")
    for fish, amount in caught_while_setlines["fish"].items():
        display = fish_displays[fish]
        stprint(f">>> {display}: x{amount}")
    stprint("\n-- Drops:\n")
    for drop, amount in caught_while_setlines["drops"].items():
        display_name = display_names["drops"][drop]
        stprint(f">>> {display_name}: x{amount}")
    stprint(f"\n{quantity} bait used.")
    
    turn+= turns_used
    manage_time()

    setting_lines = False

    
    





def show_commands():
    stprint("\n=== COMMANDS ===")
    stprint("fish / f - Cast your line and try to catch fish")
    stprint("inventory - Check your gear, fish, and items")
    stprint("rods - Switch between your fishing rods")
    stprint("baits - Change your equipped bait")
    stprint("shop - Visit the shop (day only)")
    stprint("workshop - Visit the Workshop (night only)")
    stprint("zones - Travel between fishing spots")
    stprint("setlines <quantity> - Set multiple lines at once for quick results (requires bait, reduced luck)")
    stprint("logbook - View discovered fish and info")
    stprint("home - Enter your shack")
    stprint("info - A little information about current zone")
    stprint("help - Show this list\n")

#print slowly - typewriter print
def tprint(text, delay=0.013):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()



player_name = input("Enter your name: ")

player = Player(player_name.title())

def start_game_exposition(player):
    tprint("The morning mist hangs over Brookhaven, a quiet village known for its legendary waters.", 0.03)
    time.sleep(1)

    stprint("\n=== QUICK CONTROLS ===")
    tprint("fish - Cast your line", 0.01)
    tprint("inventory - Check gear and catches", 0.01)
    tprint("shop - Buy bait or sell fish (day only)", 0.01)
    tprint("workshop - Crafting and quests (night only)", 0.01)
    tprint("zones - Travel to new fishing spots", 0.01)
    tprint("logbook - Track your discoveries", 0.01)
    tprint("help - Displays all command keys")
    time.sleep(1)
    
    tprint("\nThe water ripples gently. Your journey begins...", 0.03)
    time.sleep(1)

def manage_time():
    global turn, time_of_day, current_hour, weather_timer, current_weather
    
    weather_timer -= 1 #WEATHER
    if weather_timer <= 0:
        current_weather = random.choice(weather_types)
        weather_timer = 48
        stprint(weather_announces[current_weather])

    
    turn += 1

    #period
    #floor division finds out how many blocks have passed, ignoring remainder of turns not yet a full period.
    #if blocks passed is even (0, 2, 4...), day. If odd, night. i used AI to teach me this solution. sources from reddit, stackexchange.
    periods_passed = turn // PERIOD_LENGTH
    new_time_of_day = "day" if periods_passed % 2 == 0 else "night"

    
    if new_time_of_day != time_of_day:
        time_of_day = new_time_of_day
        if time_of_day == "day":
            print(" --- The sun rises on the horizon. It's day.")
        else:
            print(" --- The sun sets. Night falls.")

    #modulo gives me the remainder, where floor division gives the full blocks.
    
    cycle_step = turn % PERIOD_LENGTH
    
    if time_of_day == "day":
        #day starts at 6 (modulo gives 0, +6 = 6am)
        current_hour = 6 + cycle_step
    else:
        #night, 6pm
        current_hour = 18 + cycle_step
        if current_hour >= 24:
            current_hour -= 24

    print(f"--- {current_hour:02d}:00 | {time_of_day.capitalize()} | {current_weather} {weather_descs[current_weather]}")

start_game_exposition(player)
while True:

    player.inventory["baits"]["worm"] += 1

    check_quest_unlocked(player)
    
    manage_time()
    flush_input()

    command = input("> ")
    para_command = command.split() #creates list in case cmd is longer than 1
    if len(para_command) < 1:
        continue


                        
    match para_command[0]:
            case "f" | "fish":
                manage_fish()
                turn+=1
                continue
            case "shop":
                shop(player)
                turn += 1
                continue
            
            case "workshop":
                workshop(player)
                turn += 1
                continue
            
            case "inventory" | "i" | "inv":
                inventory(player)
                continue

            case "baits":
                switch_bait(player)
                for bait,quantity in player.inventory["baits"].items():
                    if quantity <=0:
                        del player.inventory["baits"][bait]
                continue

            case "rods":
                switch_rods(player)
                continue
                
            case "zones":
                switch_zone(player)
                turn += 1
                continue
                
            case "info":
                zone_info(player)
                continue
                
            case "logbook":
                logbook(player)
                continue
                
            case "commands" | "help": 
                show_commands()
                continue
            
            case "shack" | "home" | "house":
                shack(player)
                continue
        
            case "set" | "setlines":
                if not player.shack["unlocked"]:
                    print("You can't set lines yet...")
                    continue
                if len(para_command) < 2:
                    stprint("Bad usage - try again with setlines <quantity>")
                    continue
                setquantity = para_command[1]
                setlines(setquantity, player, time_of_day)

                
                
                
            case _:
                stprint("That's not a valid command.")
                continue
        
