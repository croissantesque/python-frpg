class Fish:
    def __init__(self, name, difficulty, traits, day_rarity, night_rarity, zones):
        self.name = name
        self.difficulty = difficulty
        self.traits = traits
        self.day_rarity = day_rarity
        self.night_rarity = night_rarity
        self.zones = zones

    def escape_chance(self, player_skill, time_of_day, bait):
        chance  =  (self.difficulty * 10) - (player_skill * 5)

        if "fast" in self.traits: chance +=  3
        if "strong" in self.traits: chance += 5
        if "glow" in self.traits and time_of_day ==  "night": chance -=  5
        if "camouflage" in self.traits: chance +=  5
        if "nocturnal" in self.traits: chance +=  0 if time_of_day  ==  "day" else -2.5
        if "evasive" in self.traits: chance +=  7.5
        if "jumpy" in self.traits: chance += 2.5

        match bait:
            case "worm": chance -=2
            case "insects": chance -= 6
            case "shimmerbait": chance -=10
            case "glowworms": chance -= 17
            case "golden_grubs": chance -= 25
            case "lunar_lure": chance -= 10

        return max(5, min(85,chance))
    

class SmallCarp(Fish):
    def __init__(self):
        super().__init__(
            name = "Small Carp",
            difficulty = 2,
            traits = [],
            day_rarity = "Common",
            night_rarity = "Common",
            zones = [0, 1]
        )
        self.drops = {"wood_plank": 0.25}
        

class Minnow(Fish):
    def __init__(self):
        super().__init__(
            name = "Minnow",
            difficulty = 0.5,
            traits = ["fast"],
            day_rarity = "Common",
            night_rarity = "Common",
            zones = [0, 1, 2]
        )

class PondPerch(Fish):
    def __init__(self):
        super().__init__(
            name = "Pond Perch",
            difficulty = 1.3,
            traits = ["jumpy"],
            day_rarity = "Rare",
            night_rarity = "Rare",
            zones = [0]
        )
        self.drops = {"iron_shard": 0.1}

class NightGoby(Fish):
    def __init__(self):
        super().__init__(
            name = "Night Goby",
            difficulty = 1.4,
            traits = ["nocturnal"],
            day_rarity = "Rare",
            night_rarity = "Uncommon",
            zones = [0]
        )
        self.drops = {"iron_shard": 0.1}

class Shimmerfin(Fish):
    def __init__(self):
        super().__init__(
            name = "Shimmerfin",
            difficulty = 2.5,
            traits = ["glow"],
            day_rarity = "Very Rare",
            night_rarity = "Very Rare",
            zones = [0]
        )
        self.drops = {"magical_resin": 0.75}

class Trout(Fish):
    def __init__(self):
        super().__init__(
            name = "Trout",
            difficulty = 2,
            traits = ["fast"],
            day_rarity = "Common",
            night_rarity = "Common",
            zones = [1, 2]
        )

class Bass(Fish):
    def __init__(self):
        super().__init__(
            name = "Bass",
            difficulty = 3,
            traits = ["strong"],
            day_rarity = "Common",
            night_rarity = "Uncommon",
            zones = [1]
        )
        self.drops = {"iron_shard": 0.3}

class Glowfish(Fish):
    def __init__(self):
        super().__init__(
            name = "Glowfish",
            difficulty = 4,
            traits = ["glow"],
            day_rarity = "Not Found",
            night_rarity = "Uncommon",
            zones = [1]
        )
        self.drops = {"glow_scale": 0.65}

class Frogfish(Fish):
    def __init__(self):
        super().__init__(
            name = "Frogfish",
            difficulty = 3,
            traits = ["camouflage", "jumpy"],
            day_rarity = "Rare",
            night_rarity = "Uncommon",
            zones = [1]
        )

class Silverfin(Fish):
    def __init__(self):
        super().__init__(
            name = "Silverfin",
            difficulty = 5,
            traits = ["evasive"],
            day_rarity = "Rare",
            night_rarity = "Uncommon",
            zones = [1]
        )

class CrystalKoi(Fish):
    def __init__(self):
        super().__init__(
            name = "Crystal Koi",
            difficulty = 6,
            traits = ["glow"],
            day_rarity = "Rare",
            night_rarity = "Very Rare",
            zones = [2,3]
        )

class RapidfinTrout(Fish):
    def __init__(self):
        super().__init__(
            name = "Rapidfin Trout",
            difficulty = 5,
            traits = ['fast', 'strong'],
            day_rarity = "Common",
            night_rarity='Uncommon',
            zones=[2]
        )
        self.drops = {'river_pearl': 0.23}

class BrookCarp(Fish):
    def __init__(self):
        super().__init__(
            name = "Carp",
            difficulty = 5,
            traits = ["strong"],
            day_rarity= "Common",
            night_rarity="Common",
            zones = [2]
        )

class BrookPerch(Fish):
    def __init__(self):
        super().__init__(
            name = "Perch",
            difficulty = 7,
            traits = ["jumpy"],
            day_rarity = "Uncommon",
            night_rarity="Rare",
            zones = [2,3]
        )
        self.drops = {"river_pearl": 0.2}

class Shadowfin(Fish):
    def __init__(self):
        super().__init__(
            name = "Shadowfin",
            difficulty = 6,
            traits = ['evasive', 'camouflage'],
            day_rarity = "Uncommon",
            night_rarity = "Common",
            zones=[2]
        )
        
class AzureGill(Fish):
    def __init__(self):
        super().__init__(
            name = "Azure Gill",
            difficulty=4,
            traits = ['glow', "jumpy"],
            day_rarity = "Rare",
            night_rarity="Not Found",
            zones=[2]
        )
        self.drops = {"azure_fin": 0.4}

class MoonlightGuppy(Fish):
    def __init__(self):
        super().__init__(
            name = "Moonlight Guppy",
            difficulty =6,
            traits=["glow", "fast"],
            day_rarity="Common",
            night_rarity="Very Rare",
            zones=[3]
        )
        self.drops = {"glow_scale": 0.4}

class DeepwaterSturgeon(Fish):
    def __init__(self):
        super().__init__(
            name = "Deepwater Sturgeon",
            difficulty=8,
            traits=["strong", "camouflage"],
            day_rarity="Uncommon",
            night_rarity="Rare",
            zones=[3]
        )
        self.drops = {"iron_shard": 0.3, "river_pearl": 0.1}

class PrismTrout(Fish):
    def __init__(self):
        super().__init__(
            name = "Prism Trout",
            difficulty = 9,
            traits=["glow", "evasive"],
            day_rarity="Rare",
            night_rarity="Rare",
            zones=[3]
        )
        self.drops = {"crystal_shard": 0.3, "magical_resin": 0.2}

class AbyssalAngler(Fish):
    def __init__(self):
        super().__init__(
            name = "Abyssal Angler",
            difficulty=9,
            traits=["strong", "glow"],
            day_rarity="Very Rare",
            night_rarity="Common",
            zones=[3]
        )
        self.drops = {"glow_scale": 0.5}

class LunarTrout(Fish):
    def __init__(self):
        super().__init__(
            name = "Lunar Trout",
            difficulty=7,
            traits=["nocturnal", "jumpy"],
            day_rarity="Rare",
            night_rarity="Uncommon",
            zones=[3]
        )
        self.drops={"moonstone": 0.45}

class GhostCarp(Fish):
    def __init__(self):
        super().__init__(
            name = "Ghost Carp", 
            difficulty=11,
            traits=["camouflage"],
            day_rarity="Extremely Rare",
            night_rarity='Legendary',
            zones=[3]
        )
        self.drops = {"spectral_fin": 0.8}

class SaltMullet(Fish):
    def __init__(self):
        super().__init__(
            name = "Salt Mullet",
            difficulty = 2,
            traits = ["fast"],
            day_rarity = "Common",
            night_rarity = "Common",
            zones = [4]
        )

class RedDrum(Fish):
    def __init__(self):
        super().__init__(
            name = "Red Drum",
            difficulty = 4,
            traits = ["strong"],
            day_rarity = "Uncommon",
            night_rarity = "Rare",
            zones = [4]
        )
        self.drops = {"seashell": 0.25}

class SpeckledTrout(Fish):
    def __init__(self):
        super().__init__(
            name = "Speckled Trout",
            difficulty = 4.5,
            traits = ["jumpy"],
            day_rarity = "Rare",
            night_rarity = "Uncommon",
            zones = [4]
        )
        self.drops = {"coral_fragment": 0.2}
        self.tidal = "Current"

class Flounder(Fish):
    def __init__(self):
        super().__init__(
            name = "Flounder",
            difficulty = 3.5,
            traits = ["camouflage"],
            day_rarity = "Uncommon",
            night_rarity = "Common",
            zones = [4]
        )
        self.drops = {"seashell": 0.15}
        self.tidal = "Slack"

class Snook(Fish):
    def __init__(self):
        super().__init__(
            name = "Snook",
            difficulty = 7.8,
            traits = ["evasive"],
            day_rarity = "Rare",
            night_rarity = "Very Rare",
            zones = [4]
        )
        self.drops = {"coral_fragment": 0.3, "seashell": 0.2}

class Tarpon(Fish):
    def __init__(self):
        super().__init__(
            name = "Tarpon",
            difficulty = 11.8,
            traits = ["jumpy", "strong"],
            day_rarity = "Extremely Rare",
            night_rarity = "Legendary",
            zones = [4]
        )
        self.drops = {"abyssal_crystal": 100}
        self.tidal = "Current"
