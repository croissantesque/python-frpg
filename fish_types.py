class Fish:
    def __init__(self, name, difficulty, traits, day_rarity, night_rarity, zones):
        self.name = name
        self.difficulty = difficulty
        self.traits = traits
        self.day_rarity = day_rarity
        self.night_rarity = night_rarity
        self.zones = zones

    def escape_chance(self, player_skill, time_of_day):
        """base chance of fail"""
        chance  =  (self.difficulty * 10) - (player_skill * 5)

        if "fast" in self.traits: chance +=  5
        if "strong" in self.traits: chance += 10
        if "glow" in self.traits and time_of_day ==  "night": chance -=  10
        if "camouflage" in self.traits: chance +=  10
        if "nocturnal" in self.traits: chance +=  0 if time_of_day  ==  "day" else -5
        if "evasive" in self.traits: chance +=  15
        if "jumpy" in self.traits: chance += 5

        return max(0, chance)
    

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
        self.drops = {"wood_plank": 0.2}
        

class Minnow(Fish):
    def __init__(self):
        super().__init__(
            name = "Minnow",
            difficulty = 1,
            traits = ["fast"],
            day_rarity = "Common",
            night_rarity = "Common",
            zones = [0, 1, 2]
        )

class PondPerch(Fish):
    def __init__(self):
        super().__init__(
            name = "Pond Perch",
            difficulty = 2,
            traits = ["jumpy"],
            day_rarity = "Rare",
            night_rarity = "Rare",
            zones = [0]
        )
        self.drops = {"iron_shard": 0.04}

class NightGoby(Fish):
    def __init__(self):
        super().__init__(
            name = "Night Goby",
            difficulty = 2,
            traits = ["nocturnal"],
            day_rarity = "Rare",
            night_rarity = "Uncommon",
            zones = [0]
        )
        self.drops = {"iron_shard": 0.05}

class Shimmerfin(Fish):
    def __init__(self):
        super().__init__(
            name = "Shimmerfin",
            difficulty = 3,
            traits = ["glow"],
            day_rarity = "Very Rare",
            night_rarity = "Very Rare",
            zones = [0]
        )
        self.drops = {"magical_resin": 0.4}

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
        self.drops = {"iron_shard": 0.15}

class Glowfish(Fish):
    def __init__(self):
        super().__init__(
            name = "Glowfish",
            difficulty = 4,
            traits = ["glow"],
            day_rarity = "Very Rare",
            night_rarity = "Rare",
            zones = [1]
        )
        self.drops = {"glow_scale": 0.2}

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
            day_rarity = "Very Rare",
            night_rarity = "Very Rare",
            zones = [1]
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
        self.drops = {'river_pearl': 0.1}

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
        self.drops = {"river_pearl": 0.05}

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
            night_rarity="Very Rare",
            zones=[2]
        )
        self.drops = {"azure_fin": 0.3}

