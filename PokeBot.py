import asyncio

from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.side_condition import SideCondition
from poke_env.environment.pokemon_type import PokemonType
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration
from poke_env.environment.move import Move
from poke_env.environment.status import Status

class PokeBot(Player):

    # How many pokemon the opponent has
    global eteam_size

    # If the pokemon used protect last turn
    global protect_last

    def choose_move(self, battle):

        # Moves the pokemon checks for
        protect = Move("protect")
        glare = Move("glare")
        twave = Move("thunderwave")
        toxic = Move("toxic")
        wisp = Move("willowisp")
        web = Move("stickyweb")
        bbunker = Move("banefulbunker")
        spikyshield = Move("spikyshield")


        # Statuses the bot checks for
        faint1 = Status(2)
        toxic2 = Status(7)

        #stats of the active enemy pokemon
        estat = battle.opponent_active_pokemon.base_stats

        #stats of the bots active pokemon
        mystat = battle.active_pokemon.base_stats

        #used to find how many pokemon the enemy has
        self.eteam_size = 6
        for enemy in battle.opponent_team:
            if battle.opponent_team[enemy].status== 2 or battle.opponent_team[enemy].status == faint1:
                self.eteam_size-=1

        # protect_last should be made False at the start of every battle
        if battle.turn == 1:
            self.protect_last = False

        # checks if the enemy pokemon is dynamaxed
        if battle.dynamax_turns_left == None:

            # Checks if the active pokemon has certain non damaging moves and uses them if conditions are met
            for m in battle.available_moves:
               # print(str(m)+" : " + str(m.id))

                # use sticky web if the opponent has more than 4 pokemon alive
                if m.id == web.id and self.eteam_size>=4:
                    print(battle.battle_tag)
                    immune = False
                    # checks if opponent already has sticky web
                    for condition in battle.opponent_side_conditions:
                        if condition == SideCondition.STICKY_WEB:
                            immune = True
                    if not immune:
                     return self.create_order(m)

                # uses protect if the opponent's active pokemon is badly poisoned
                if (m.id==protect.id or m.id == spikyshield.id or m.id == bbunker.id) \
                        and (battle.opponent_active_pokemon.status==toxic2 or
                                         battle.opponent_active_pokemon.status==7):
                    # checks if the active pokemon didn't use it last turn
                    if self.protect_last == False:
                        self.protect_last = True
                        return self.create_order(m)
                    else:
                        self.protect_last = False

                # checks if the opponent's pokemon doesn't have another status
                if m.id==glare.id and battle.opponent_active_pokemon.status==None:
                    immune = False
                    # checks if the enemy pokemon is immune
                    for type in battle.opponent_active_pokemon.types:
                        if type == PokemonType.ELECTRIC:
                            immune = True
                    # uses glare if the opponent not immune and is faster than the active pokemon
                    if not immune and estat["spe"]>=mystat["spe"]:
                        return self.create_order(m)

                # checks if the opponent's pokemon doesn't have another status
                if m.id==twave.id and battle.opponent_active_pokemon.status==None:
                    immune = False
                    # checks if the enemy pokemon is immune
                    for type in battle.opponent_active_pokemon.types:
                        if type == PokemonType.ELECTRIC or type == PokemonType.GROUND:
                            immune = True
                    # uses thunder wave if the opponent is not immune and is faster than the active pokemon
                    if not immune and estat["spe"] >= mystat["spe"]:
                        return self.create_order(m)

                # checks if the opponent's pokemon doesn't have another status
                if m.id==toxic.id and battle.opponent_active_pokemon.status==None:
                    immune = False
                    species = battle.active_pokemon.species

                    # checks if the opponent's pokemon is immune
                    for type in battle.opponent_active_pokemon.types:
                        if type == PokemonType.POISON or type == PokemonType.STEEL:
                            immune = True

                    # uses toxic if the enemy is not immune or if the active pokemon is salazzle (which has corrosion)
                    if ((not immune) or (species.lower=="salazzle")):
                        return self.create_order(m)

                # checks if the opponent's pokemon doesn't have another status
                if m.id==wisp.id and battle.active_pokemon.status==None:
                    immune = False
                    # checks if the opponent is immune
                    for type in battle.opponent_active_pokemon.types:
                        if type == PokemonType.FIRE:
                            immune = True

                    # uses wil o wisp if the enemy isn't immmune and is a physical attacker
                    if not immune and estat["atk"] >= mystat["spa"]:
                        return self.create_order(m)

        # switches to a new pokemon if the active pokemon fainted or has a debuffed attack or special attack stat
        if (battle.active_pokemon.fainted or battle.active_pokemon.boosts["atk"]<= -2  or battle.active_pokemon.boosts["spa"]<= -2) and len(battle.available_switches)>0:
            return switch(self,battle)

        if battle.available_moves:

            damages = [0, 0, 0, 0]

            # finds how much damage each move deals
            for i in range(len(battle.available_moves)):

                # damage calculations are found using the damageCalc helper method
                damages[i] = damageCalc(battle.active_pokemon,battle.opponent_active_pokemon, battle.available_moves[i], battle.weather, battle.fields)
            index = 0
            max = 0
            # finds the move that deals the most damage
            for i in range (len(battle.available_moves)):
                if max < damages[i]:
                    max = damages[i]
                    index = i

            if len(battle.available_switches) == 0 and battle._can_dynamax:
                # uses the move that deals the most damage
                return self.create_order(battle.available_moves[index],dynamax=True)

            else:
                return self.create_order(battle.available_moves[index])

        # no moves available so switch
        elif(len(battle.available_switches)!=0):
            return switch(self,battle)
        else:
            return self.choose_random_move(battle)



# used to find the move that deals the most damage
def damageCalc(my_poke, opp_poke, move,weather,terrain):

    damage = move.base_power

    # takes into account skill link
    if move.expected_hits>2:
        damage*=5
    else:
        damage*=move.expected_hits

    # Accounts for abilities that make pokemon immune to certain attacks
    for j in opp_poke.possible_abilities:
        i = opp_poke.possible_abilities[j]

        if i == "Levitate" and move.type==PokemonType.GROUND:
            damage*=0
        if i == "Flash Fire"and move.type==PokemonType.FIRE:
            damage*=0

        if i == "Lightning Rod"and move.type==PokemonType.ELECTRIC:
            damage*=0

        if i == "Motor Drive"and move.type==PokemonType.ELECTRIC:
            damage*=0

        if i == "Volt Absorb"and move.type==PokemonType.ELECTRIC:
            damage*=0

        if i == "Water Absorb"and move.type==PokemonType.WATER:
            damage*=0

        if i == "Dry Skin"and move.type==PokemonType.WATER:
            damage*=0

        if i == "Sap Sipper"and move.type==PokemonType.GRASS:
            damage*=0

        if i == "Storm Drain"and move.type==PokemonType.WATER:
            damage*=0

    # accounts for STAB
    for i in my_poke.types:
        if i == move.type:
            damage *= 1.5

    # accounts for effectiveness
    damage *= move.type.damage_multiplier(opp_poke.type_1, opp_poke.type_2)

    # accounts for weather
    if weather != None:
        if weather.RAINDANCE == weather:
            if move.type == PokemonType.WATER:
                damage*=1.5

            if move.type == PokemonType.FIRE:
                damage *=.677777


        if weather.SUNNYDAY == weather:
            if move.type == PokemonType.FIRE:
                damage *= 1.5
            if move.type == PokemonType.WATER:
                damage *= .677777

    # accounts for terrain
    for field in terrain:
        if field == field.ELECTRIC_TERRAIN:
            if move.type == PokemonType.ELECTRIC:
                damage *= 1.3

        if field == field.MISTY_TERRAIN:
            if move.type == PokemonType.DRAGON:
                damage *= .5

        if field == field.PSYCHIC_TERRAIN:
            if move.type == PokemonType.PSYCHIC:
                damage*= 1.3
        if field == field.GRASSY_TERRAIN:
            if move.type == PokemonType.GRASS:
                damage*= 1.3
            if move.type == PokemonType.GROUND:
                damage*=.5

    return damage

# used to decide what pokemon to switch into
def switch(player, battle):
    index2 = 0
    max2 = 0

    # Switches to a pokemon with an effective typing
    for i in range(len(battle.available_switches)):
        if battle.opponent_active_pokemon.damage_multiplier(battle.available_switches[i].type_1) > max2:
            index2 = i
            max2 = battle.opponent_active_pokemon.damage_multiplier(battle.available_switches[i].type_1)
        if battle.opponent_active_pokemon.damage_multiplier(battle.available_switches[i].type_2) > max2:
            index2 = i
            max2 = battle.opponent_active_pokemon.damage_multiplier(battle.available_switches[i].type_2)

    # If no pokemon has an effective typing, it switches into a pokemon that resists
    if max2 <= 1:
        max2 = 4
        index2 = 0
        for i in range(len(battle.available_switches)):
            if battle.available_switches[i].damage_multiplier(battle.opponent_active_pokemon.type_1) < max2:
                index2 = i
                max2 = battle.available_switches[i].damage_multiplier(battle.opponent_active_pokemon.type_1)
    if len(battle.available_switches) != 0:
        return player.create_order(battle.available_switches[index2])

