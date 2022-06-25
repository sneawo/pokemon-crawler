from rest_framework import routers
from pokemons import views


router = routers.DefaultRouter()
router.register(r"pokemons", views.PokemonViewSet)
