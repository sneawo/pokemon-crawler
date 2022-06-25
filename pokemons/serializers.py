from rest_framework import serializers
from pokemons import models


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pokemon
        fields = "__all__"
