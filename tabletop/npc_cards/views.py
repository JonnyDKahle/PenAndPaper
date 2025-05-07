from django.shortcuts import render, get_object_or_404
from .models import NPCCharacter, Universe, Location
from .forms import LocationForm

# Create your views here.

def index(request):
    return render(request, 'npc_cards/index.html')

def NPCCharacterCardsView(request):
    all_characters = NPCCharacter.objects.all()

    context = {'npc_cards':all_characters}
    return render(request, 'npc_cards/npc_charactercards.html', context=context)

def UniverseView(request):
    all_universes = Universe.objects.all()

    context = {'all_universes':all_universes}
    return render(request, 'npc_cards/universes.html', context=context)

def LocationDetailView(request, id):
    location = get_object_or_404(Location, id=id)

    context = {'location':location}
    return render(request, 'npc_cards/location_detail.html', context=context)

# def CreateNPCInstaceView(request):
#     if request.method == 'POST':
#         form = NPCInstanceForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = NPCInstanceForm

#     context = {'form':form}
#     return render(request, 'npc_cards/npcinstance_create.html', context=context)
