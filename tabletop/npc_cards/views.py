from django.shortcuts import render, get_object_or_404, redirect
from .models import NPCCharacter, Universe, Location
from .forms import LocationForm, NPCCharacterForm, NPCCharacterFormBlueprintForm

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

def blueprint_list(request):
    """Show all character blueprints"""
    blueprints = NPCCharacter.objects.filter(is_blueprint=True)
    context = {'blueprints':blueprints}
    return render(request, 'npc_cards/blueprint_list.html', context=context)

def character_list(request):
    """Show all character instances"""
    characters = NPCCharacter.objects.filter(is_blueprint=False)
    context = {'characters':characters}
    return render(request, 'npc_cards/character_list.html', context=context)

def character_detail(request, id):
    """Show details for a character"""
    character = get_object_or_404(NPCCharacter, id=id)
    context = {'character':character}
    return render(request, 'npc_cards/character_detail.html', context=context)

def create_blueprint(request):
    """Create a new character blueprint"""
    if request.method == 'POST':
        form = NPCCharacterForm(request.POST, request.FILES)
        if form.is_valid():
            blueprint = form.save(commit=False)
            blueprint.is_blueprint = True
            blueprint.save()

            # Save M2M fields
            form.save_m2m()

            return redirect('npc_cards:blueprint_detail', id=blueprint.id)
    else:
        form = NPCCharacterForm()

    return render(request, 'npc_cards/blueprint_form.html', {'form':form})

def create_character(request):
    """Create a new character, optionally based on a blueprint"""
    form = NPCCharacterForm()
    blueprints = NPCCharacter.objects.filter(is_blueprint=True)
    blueprint_form = NPCCharacterFormBlueprintForm()

    if request.method == 'POST':
        # Check if a blueprint was selected
        blueprint_id = request.POST.get('blueprint')

        if blueprint_id:
            # Creating form blueprint
            blueprint = get_object_or_404(NPCCharacter, id=blueprint_id, is_blueprint=True)
            form = NPCCharacterFormBlueprintForm(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name']
                location = form.cleaned_data['location']

                # Create instance from blueprint
                character = blueprint.create_instance(
                    instance_name=name,
                    location=location
                )
                return redirect('npc_cards:character_detail', id=character.id)
        else:
            # Creating from scratch
            form = NPCCharacterForm(request.POST, request.FILES)
            if form.is_valid():
                character = form.save(commit=False)
                character.is_blueprint = False
                character.save()
                form.save_m2m()
                return redirect('npc_cards:character_detail', id=character.id)
    else:
        # Initial form load - show both options
        form = NPCCharacterForm()
        blueprints = NPCCharacter.objects.filter(is_blueprint=True)
        blueprint_form = NPCCharacterFormBlueprintForm()

    context = {
        'form':form,
        'blueprints':blueprints,
        'blueprint_form':blueprint_form,
    }
    return render(request, 'npc_cards/character_form.html', context=context)

def edit_character(request, id):
    """Edit a character"""
    character = get_object_or_404(NPCCharacter, id=id)

    if request.method == 'POST':
        form = NPCCharacterForm(request.POST, request.FILES, instance=character)
        if form.is_valid():
            form.save()
            return redirect('npc_cards:character_detail', id=character.id)
    else:
        form = NPCCharacterForm(instance=character)

    context = {
        'form':form,
        'character':character,
    }
    return render(request, 'npc_cards/character_edit.html', context=context)

def edit_blueprint(request, id):
    blueprint = get_object_or_404(NPCCharacter, id=id)

    if request.method == 'POST':
        form = NPCCharacterFormBlueprintForm(request.POST, request.FILES, instance=blueprint)
        if form.is_valid():
            form.save()
            return redirect('npc_cards:blueprint_detail', id=blueprint.id)
    else:
        form = NPCCharacterFormBlueprintForm(instance=blueprint)
    
    context = {
        'form':form,
        'blueprint':blueprint,
        'has_instances': NPCCharacter.objects.filter(blueprint=blueprint).exists(),
    }
    return render(request, 'npc_cards/blueprint_edit.html', context=context)