# I am using this bot to help practice using the poke-env library and see what useful information I can use to make a
# strategic decision
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
import json


class ScanBot(Player):

    # Prints useful information to the console. Then, makes a random move.
    def choose_move(self, battle):

        print("___________Turn #" + str(battle.turn) + "___________")

        # All Available moves
        print("~~~~~MOVES~~~~~")
        print("Available Switches: ", battle.available_switches)
        print("Available Moves: ", battle.available_moves)

        # Active Pokemon
        print("~~~~~Active Pokemon~~~~~")

        print("Opp Pokemon: ", battle.opponent_active_pokemon)
        print("My Pokemon: ", battle.active_pokemon)

        # Stats of my Pokemon
        print("~~~~~My STATS~~~~~")
        print("My level: ", battle.active_pokemon.level)
        print("My Stats: ", battle.active_pokemon.stats)
        print("My Item: ", battle.active_pokemon.item)
        print("My Ability: ", battle.active_pokemon.ability)

        # Stats of Enemy Pokemon
        print("~~~~~Enemy STATS~~~~~")
        print("Enemy level: ", battle.opponent_active_pokemon.level)
        print("Enemy Stats: ", battle.opponent_active_pokemon.stats)
        print("Enemy Item: ", battle.opponent_active_pokemon.item)
        print("Enemy Ability: ", battle.opponent_active_pokemon.ability)

        # Stat boosts
        print("~~~~~BOOSTS~~~~~")
        print("My Boosts: ", battle.active_pokemon.boosts)
        print("Enemy Boosts: ", battle.opponent_active_pokemon.boosts)

        # The fields
        print("~~~~~FIELD~~~~~")
        print("Fields: ", battle.fields)
        print("Weather: ", battle.weather)
        print("My Side Conditions: ", battle.side_conditions)
        print("Opp Side Conditions: ", battle.opponent_side_conditions)

        return self.choose_random_move(battle)


async def main():
    # Insert the username and password of the bot
    bot_name = ""
    bot_password = ""
    
    # Insert your name here
    your_name = ""

    player = ScanBot(
        player_configuration=PlayerConfiguration(bot_name, bot_password),
        server_configuration=ShowdownServerConfiguration, start_timer_on_battle_start=True
    )

    # Makes the bot challenge you
    await player.send_challenges(your_name, n_challenges=10)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
