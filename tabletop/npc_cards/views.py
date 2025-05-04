from django.shortcuts import render
from .models import NPCCharacterCard, Universe

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

# def LocationView(request):
#     specific