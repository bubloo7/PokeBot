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

        print("Available Switches: ", battle.available_switches)
        print("Available Moves: ", battle.available_moves)

        print("Opp Pokemon: ", battle.opponent_active_pokemon)
        print("My Pokemon: ", battle.active_pokemon)
        print("My Pokemon Species: ", battle.active_pokemon.species)

        print("My level: ", battle.active_pokemon.level)
        print("My Stats: ", battle.active_pokemon.stats)

        print("My Boosts: ", battle.active_pokemon.boosts)
        print("Enemy Boosts: ", battle.opponent_active_pokemon.boosts)

        print("Fields: ", battle.fields)
        print("My Side Conditions: ", battle.side_conditions)
        print("Opp Side Conditions: ", battle.opponent_side_conditions)

        return self.choose_random_move(battle)


async def main():
    # Insert the username and password of the bot
    bot_name = ""
    bot_password = ""

    player =  ScanBot(
        player_configuration=PlayerConfiguration(bot_name,bot_password),
        server_configuration=ShowdownServerConfiguration, start_timer_on_battle_start=True
    )

    # Makes the bot open to challenges so you can challenge it
    await player.accept_challenges(None, 100)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())