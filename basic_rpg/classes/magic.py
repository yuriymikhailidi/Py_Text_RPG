import random

class Spell:
    def __init__(self, name, cost, dmg, type_spell):
        self.name = name
        self.cost = cost
        self.type_spell = type_spell
        self.dmg = dmg

    def generate_spell_dmg(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)
