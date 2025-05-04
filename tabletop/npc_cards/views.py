from django.shortcuts import render
from .models import NPCCharacterCard, Universe, Location

# Create your views here.

def index(request):
    return render(request, 'npc_cards/index.html')

def NPCCharacterCardsView(request):
    all_characters = NPCCharacterCard.objects.all()

    context = {'npc_cards':all_characters}
    return render(request, 'npc_cards/npc_charactercards.html', context=context)

def UniverseView(request):
    all_universes = Universe.objects.all()

    context = {'all_universes':all_universes}
    return render(request, 'npc_cards/universes.html', context=context)

def LocationDetailView(request, id):
    location = Location.objects.get(id=id)

    context = {'location':location}
    return render(request, 'npc_cards/location_detail.html', context=context)