from classes.game import Person, Colors
from classes.magic import Spell
from classes.inventory import Item

import random

#Player Magic
#Create Black Magic
fire = Spell("Fire", 20, 100, "black")
thunder = Spell("Thunder", 20, 100, "black")
blizzard= Spell("Blizzard", 25, 100, "black")
meteor = Spell("Meteor", 50, 200, "black")
quake = Spell("Quake", 60, 120, "black")

#Create White Magic
cure  = Spell("Cure", 16, 120, "white")
cura  = Spell("Cura", 25, 200, "white")

#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Potion", "potion", "Heals 400 HP", 400)
elixer = Item("Elixer", "elixer", "Restore all MP/HP of one person", 9999)
superelixer = Item("Elixer", "elixer", "Restore all group MP/HP", 9999)

#Attack Item
runestone = Item("Rune Stone", "attack", "Deals 200 dmg", 200)

spells = [{"name": "Fire", "cost": 10, "dmg": 60},
        {"name": "Thunder", "cost": 10, "dmg": 120},
        {"name": "Blizzard", "cost": 10, "dmg": 130}]

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "amount": 10}, {"item": hipotion, "amount": 5}, {"item": superpotion, "amount": 2}, 
                {"item": elixer, "amount": 2}, {"item": superelixer, "amount": 2},{"item": runestone, "amount": 2}]
player1 = Person("Dranel", 1200, 120, 60, 34, player_magic, player_items)
player2 = Person("Athiel", 1200, 150, 60, 34, player_magic, player_items)
player3 = Person("Talgel", 1200, 174, 60, 34, player_magic, player_items)

enemy1 = Person("Smaller Demon", 1000, 200, 75, 25, enemy_spells, [])
enemy2 = Person("Vuzemon", 2200, 500, 125, 25, enemy_spells, [])
enemy3 = Person("Smaller Demon", 1000, 200, 75, 25, enemy_spells, [])

i = 0
run = True

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
while run:
    print("===================")        
    print("\n""\n")
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose Action: ")
        index = int(choice) - 1
    
        if index == 0:
            
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("     Target: "+ Colors.FAIL + enemies[enemy].name + Colors.ENDC + " Your attack was:", dmg, "points of damage. Enemy HP:", enemies[enemy].get_hp())

            if enemies[enemy].get_hp() == 0:
                print("     " + Colors.FAIL + enemies[enemy].name + Colors.ENDC + " has been banished back to HELL")
                del enemies[enemy]

        elif index == 1:
            
            player.choose_spell()
            spell_choice = int(input("Choose Magic Atk: ")) - 1

            if spell_choice == -1:
                continue
            
            #Player Choice Of Magic
            spell = player.magic[spell_choice]
            magic_dmg = spell.generate_spell_dmg()

            current_mp = player.get_mp()
            
            if spell.cost > current_mp:
                print(Colors.FAIL + "You cant cast this spell" + Colors.ENDC)
                continue
            
            player.reduce_mp(spell.cost)
            
            if spell.type_spell == "white":
                player.heal(magic_dmg)
                print(Colors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_dmg), " HP. " + Colors.ENDC)
            
            elif spell.type_spell == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(dmg)
                print("     Target: " + Colors.FAIL + enemies[enemy].name + Colors.ENDC + Colors.OKBLUE + "\n" + spell.name + " deals ", str(magic_dmg), " points of damage" + Colors.ENDC)
            
                if enemies[enemy].get_hp() == 0:
                    print("     " + Colors.FAIL + enemies[enemy].name + Colors.ENDC + " has been banished back to HELL")
                    del enemies[enemy]

            elif index == 2:
                player.choose_item()
                item_choice = int(input("Choose Item: ")) - 1
                
                if item_choice == -1:
                    continue
                
                item = player.item[item_choice]["item"]
                
                if player.item[item_choice]["amount"]  == 0:
                    print(Colors.FAIL + "\n" + "No Items left" + Colors.ENDC)
                    continue
                
                player.item[item_choice]["amount"] -= 1
            
                if item.item_type == "potion":
                    player.heal(item.prop)
                    print(Colors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + Colors.ENDC)
                elif item.item_type == "elixer":
                    if item.name == "superelixer":
                        for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(Colors.OKGREEN + "\n" + item.name + " heals all damage and restores all magic" + Colors.ENDC)
                elif item.item_type == "attack":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print("     Target: " + Colors.FAIL + enemies[enemy].name + Colors.ENDC + Colors.WARNING + "\n" + item.name + " deals", str(item.prop), "points of damage" + Colors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print("     " + Colors.FAIL + enemies[enemy].name + Colors.ENDC + " has been banished back to HELL")
                        del enemies[enemy]

    #Chece if the battle ended
    defeated_en = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_en += 1
    for pl in players:
        if pl.get_hp() == 0:
            defeated_players += 1
    if defeated_en == 2:
        print(Colors.OKGREEN + "You win!" + Colors.ENDC)
        run = False
    elif defeated_players == 2:
        print(Colors.FAIL + "You lost!" + Colors.ENDC)
        run = False

    #Enemy Move
    
    for enemy in enemies:     
        enemy_choice = random.randint(0, 3)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(Colors.FAIL + enemy.name + "attacked" + players[target] + "for "+ str(enemy_dmg) + Colors.ENDC)
        if enemy_choice == 1:
            spell, magic_damage = enemy.generate_spell()
            enemy.reduce_mp(magic_damage)
            print("\n" + "     Enemy used " + spell.name)
            if spell.type_spell == "white":
                enemy.heal(magic_damage)
                print(Colors.OKBLUE + "\n Enemy used " + spell.name + " healed for ", str(magic_damage), " HP. " + Colors.ENDC)
                
            elif spell.type_spell == "black":
                target = random.randint(0, 3)
                players[target].take_damage(magic_damage)
                print("     Target: " + Colors.FAIL + players[target].name + Colors.ENDC + Colors.OKBLUE + "\n" + spell.name + " deals ", str(magic_damage), " points of damage" + Colors.ENDC)
                
                if players[target].get_hp() == 0:
                    print("     " + Colors.FAIL + players[target].name + Colors.ENDC + " has been slayed")
                    del players[target]