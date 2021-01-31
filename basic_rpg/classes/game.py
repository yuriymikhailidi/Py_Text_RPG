import random
import pprint
from .magic import Spell


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m' 
class Person:
    def __init__(self, name, hp, mp, atk, df, magic, item):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkh = atk + 10
        self.atkl = atk - 10
        self.df = df
        self.magic = magic
        self.item = item
        self.actions = ['Attack', 'Magic', 'Items']
    
    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp
    
    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp
    
    def get_hp(self):
        return self.hp
    
    def get_maxh(self):
        return self.maxhp
    
    def get_mp(self):
        return self.mp
    
    def get_max_mp(self):
        return self.maxmp


    def reduce_mp(self, cost):
        self.mp -= cost
    def choose_target(self, enemies):
        i = 1
        print("     " + Colors.FAIL + Colors.BOLD  + "TARGETS\n" + Colors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("     " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    Choose Enemy: ")) - 1
        return choice

    def choose_action(self):
        i = 1
        print("\n" + Colors.BOLD + self.name + Colors.ENDC)  
        print(Colors.WARNING + "    Actions\n" + Colors.ENDC)
        for item in self.actions:
            print("     " + str(i) + ":", item)
            i += 1
    def choose_spell(self):
        i = 1
        print("     " + Colors.OKBLUE + Colors.BOLD  + "MAGIC\n" + Colors.ENDC)
        for spell in self.magic:
            print("     " + str(i) + ":", spell.name, "(Cost: ", str(spell.cost), ")")
            i += 1

    def choose_item(self):
        i = 1
        print("     " + Colors.WARNING + Colors.BOLD  + "ITEMS\n" + Colors.ENDC)
        for item in self.item:
            print("     " + str(i) + ". ", item["item"].name + ":", item["item"].description, "(x" + str(item["amount"]) + ")")
            i += 1
    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 4
        if self.name == "Smaller Demon":
            print("                           _________________________")
        else:
            print("                     _________________________")
        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "
        
        hp_string  = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decrease = 9 - len(hp_string)
            
            while decrease > 0:
                current_hp += " "
                decrease -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string
        
        print(Colors.BOLD + self.name + "   "+ current_hp + " |" + Colors.FAIL + hp_bar + Colors.ENDC + "|   " + Colors.ENDC)

    def get_stats(self):
        hp_bar = ""
        hp_bar_ticks = (self.hp / self.maxhp) * 100 / 4
        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        mp_bar = ""
        mp_bar_ticks = (self.mp / self.maxmp) * 100 / 10
        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "
        
        hp_string  = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decrease = 9 - len(hp_string)
            
            while decrease > 0:
                current_hp += " "
                decrease -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string  = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)
            
            while decreased > 0:
                current_mp += " "
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string
        print("                     _________________________             __________ ")
        print(Colors.BOLD + self.name + "    "+ current_hp + " |" + Colors.OKGREEN + hp_bar + Colors.ENDC + "|   "  + current_mp + " |"+ Colors.OKBLUE + mp_bar + Colors.ENDC + "|" + Colors.ENDC)

    def generate_spell(self):
        mg_choice = random.randint(0, len(self.magic))
        spell = self.magic[mg_choice]
        dmg = spell.generate_spell_dmg()
        
        hp_pct = self.hp / self.maxhp * 100


        if self.mp < spell.cost or spell=="white" and hp_pct > 50:
            self.generate_spell()
        else:
            return spell, dmg