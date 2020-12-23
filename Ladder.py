from PokeBot import PokeBot
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration
import asyncio

async def main():
    # fill in the account details to the account you want the bot to log into below
    username = ""
    password = ""

    # fill in with how many games you want the bot to play
    games = 0

    # creates the bot with the given username and password
    player =  PokeBot(
        player_configuration=PlayerConfiguration(username,password),
        server_configuration=ShowdownServerConfiguration,
    )
    await player.ladder(0)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
