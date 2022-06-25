from rest_framework import viewsets
from pokemons import models, serializers


class PokemonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to view pokemons.
    """

    queryset = models.Pokemon.objects.all()
    serializer_class = serializers.PokemonSerializer
