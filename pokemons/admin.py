from django.contrib import admin
from django.utils.html import format_html

from pokemons.models import Pokemon, PokemonAbility


class PokemonAbilityInline(admin.TabularInline):
    model = PokemonAbility


class PokemonAdmin(admin.ModelAdmin):
    list_display = ("image", "name", "weight", "height", "abilities")
    inlines = (PokemonAbilityInline,)

    def image(self, obj):
        return format_html(f'<img src="{obj.image_url}"/>')  # TODO: check if url field has protection from xss

    def abilities(self, obj):
        return ", ".join(obj.abilities.values_list("name", flat=True))


admin.site.register(Pokemon, PokemonAdmin)
