import folium
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_pokemon_entities(pokemon_id):
    current_datetime = localtime()
    return PokemonEntity.objects.filter(
        pokemon=pokemon_id,
        appeared_at__lte=current_datetime,
        disappeared_at__gte=current_datetime,
    )


def get_pokemon_image_url(request, pokemon_image):
    return request.build_absolute_uri(pokemon_image.url) if pokemon_image else DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_image_url = get_pokemon_image_url(request, pokemon.image)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_url,
            'title_ru': pokemon.title,
        })

        pokemon_entities = get_pokemon_entities(pokemon)
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon_image_url
            )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon_entities = get_pokemon_entities(pokemon_id)
    pokemon_image_url = get_pokemon_image_url(request, pokemon.image)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image_url
        )

    previous_evolution = {}
    if pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': get_pokemon_image_url(request, pokemon.previous_evolution.image),
        }

    next_evolution = {}
    next_evolution_pokemon = pokemon.next_evolutions.first()
    if next_evolution_pokemon:
        next_evolution = {
            'pokemon_id': next_evolution_pokemon.id,
            'title_ru': next_evolution_pokemon.title,
            'img_url': get_pokemon_image_url(request, next_evolution_pokemon.image),
        }

    return render(
        request, 'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': {
                'title_ru': pokemon.title,
                'title_en': pokemon.title_en,
                'title_jp': pokemon.title_jp,
                'description': pokemon.description,
                'img_url': pokemon_image_url,
                'previous_evolution': previous_evolution,
                'next_evolution': next_evolution,
            }
        })
