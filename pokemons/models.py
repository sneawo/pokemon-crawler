from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=256)
    weight = models.IntegerField()
    height = models.IntegerField()
    image_url = models.URLField()


class PokemonAbility(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name="abilities", on_delete=models.CASCADE)
    name = models.CharField(max_length=256)  # here we can use fk to Ability model
    is_hidden = models.BooleanField()
    slot = models.IntegerField()
