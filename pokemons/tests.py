from unittest import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pokemons.models import Pokemon
from pokemons import crawler


class BooksViewSetTests(APITestCase):
    def test_get_books_list(self):
        Pokemon.objects.bulk_create(Pokemon(id=i, name=str(i), weight=i, height=i) for i in range(5))

        url = reverse("pokemon-list")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        assert len(data) == 5


class CrawlerSavePokemonsTests(TestCase):
    def test_create_pokemon(self):
        pokemon_dict = {
            "id": 1,
            "name": "bulbasaur",
            "weight": 69,
            "height": 7,
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
            },
            "abilities": [{"ability": {"name": "run-away"}, "is_hidden": True, "slot": 1}],
        }
        crawler._save_pokemons([pokemon_dict])
        pokemon = Pokemon.objects.get(id=1)
        assert pokemon.name == "bulbasaur"
        assert pokemon.weight == 69
        assert pokemon.height == 7
        abilities = pokemon.abilities.all()
        assert len(abilities) == 1
        assert abilities[0].name == "run-away"
        assert abilities[0].is_hidden
        assert abilities[0].slot == 1

    def test_update_pokemon(self):
        pokemon = Pokemon(id=1, name="test", weight=0, height=0, image_url="")
        pokemon.save()
        pokemon.abilities.create(name="test1", is_hidden=False, slot=0)

        pokemon_dict = {
            "id": 1,
            "name": "bulbasaur",
            "weight": 69,
            "height": 7,
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
            },
            "abilities": [{"ability": {"name": "run-away"}, "is_hidden": True, "slot": 1}],
        }
        crawler._save_pokemons([pokemon_dict])
        pokemon = Pokemon.objects.get(id=1)
        assert pokemon.name == "bulbasaur"
        assert pokemon.weight == 69
        assert pokemon.height == 7
        abilities = pokemon.abilities.all()
        assert len(abilities) == 1
        assert abilities[0].name == "run-away"
        assert abilities[0].is_hidden
        assert abilities[0].slot == 1


# TODO: tests for other functions in crawler
