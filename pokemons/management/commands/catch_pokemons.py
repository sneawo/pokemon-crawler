import asyncio
from django.core.management.base import BaseCommand
from pokemons.crawler import catch_pokemons


class Command(BaseCommand):
    help = "Find pokemons and load them to db"

    def handle(self, *args, **options):
        catch_pokemons()
        self.stdout.write(self.style.SUCCESS("done"))
