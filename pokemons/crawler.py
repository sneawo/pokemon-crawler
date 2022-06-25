import asyncio
import aiohttp
import logging

from asgiref.sync import async_to_sync

from pokemons.models import Pokemon

logger = logging.getLogger(__name__)

# can be placed in config and read from env variables
API_URL = "https://pokeapi.co/api/v2/pokemon"
TIMEOUT = aiohttp.ClientTimeout(sock_connect=2, sock_read=10)
LIMIT = 20


async def _find_pokemons() -> list[dict]:
    """I used asyncio approach, but it can be done with threads or celery tasks."""
    params = {"limit": LIMIT}  # better to use pagination
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params, timeout=TIMEOUT) as response:
            data = await response.json()  # TODO: process errors
            tasks = [_get_pokemon(session, pokemon["url"]) for pokemon in data["results"]]
            pokemons = await asyncio.gather(*tasks)  # would be good to add ratelimiter
            logger.info(f"action=find_pokemons, status=success, number={len(pokemons)}")
            return pokemons


async def _get_pokemon(session: aiohttp.ClientSession, pokemon_url: str) -> dict:
    async with session.get(pokemon_url, timeout=TIMEOUT) as response:
        data = await response.json()  # TODO: process errors
        return data


def _save_pokemons(pokemons: list[dict]) -> None:
    def update_pokemon(pokemon: Pokemon, pokemon_dict: dict) -> None:
        pokemon.name = pokemon_dict["name"]
        pokemon.weight = pokemon_dict["weight"]
        pokemon.height = pokemon_dict["height"]
        pokemon.image_url = pokemon_dict["sprites"].get("front_default")

    def add_abilities(pokemon: Pokemon, abilities: list[dict]) -> None:
        for ability in abilities:
            pokemon.abilities.create(
                name=ability["ability"]["name"], is_hidden=ability["is_hidden"], slot=ability["slot"]
            )

    for pokemon_dict in pokemons:
        pokemon_id = pokemon_dict["id"]
        pokemon = Pokemon.objects.filter(id=pokemon_id).first()
        if pokemon:
            pokemon.abilities.all().delete()
        else:
            pokemon = Pokemon(id=pokemon_id)

        update_pokemon(pokemon, pokemon_dict)
        pokemon.save()  # for performance better to use bulk_create, bulk_update
        add_abilities(pokemon, pokemon_dict.get("abilities", []))

    logger.info("action=save_pokemons, status=success")


def catch_pokemons() -> None:
    pokemons = async_to_sync(_find_pokemons)()
    _save_pokemons(pokemons)
