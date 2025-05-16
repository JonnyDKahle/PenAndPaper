from django.shortcuts import render, get_object_or_404, redirect
from .models import NPCCharacter, Universe, Location, Item
from .forms import LocationForm, NPCCharacterForm, NPCCharacterFormBlueprintForm, NPCCharacterBlueprintEditForm
from .forms import NPCCharacterBlueprintForm, ItemCreateForm, SimpleLocationForm

# Create your views here.

def index(request):
    return render(request, 'npc_cards/index.html')

def NPCCharacterCardsView(request):
    all_characters = NPCCharacter.objects.filter(creator=request.user)

    context = {'npc_cards':all_characters}
    return render(request, 'npc_cards/npc_charactercards.html', context=context)

def UniverseView(request):
    all_universes = Universe.objects.filter(creator = request.user)
    other_universes = Universe.objects.exclude(creator = request.user)

    context = {
        'all_universes':all_universes,
        'other_universes':other_universes,
        }
    return render(request, 'npc_cards/universes.html', context=context)

def LocationDetailView(request, id):
    location = get_object_or_404(Location, id=id)
    
    # Initialize all forms
    item_form = ItemCreateForm()
    character_form = NPCCharacterForm(initial={'location': location})
    sublocation_form = SimpleLocationForm()
    parent_form = SimpleLocationForm()
    
    if request.method == 'POST':
        if 'submit_item' in request.POST:
            # Process item form (existing code)
            item_form = ItemCreateForm(request.POST)
            if item_form.is_valid():
                item = item_form.save()
                location.items.add(item)
                return redirect('npc_cards:location', id=location.id)
            
        elif 'submit_character' in request.POST:
            # Process character form (existing code)
            character_form = NPCCharacterForm(request.POST, request.FILES)
            if character_form.is_valid():
                character = character_form.save(commit=False)
                character.is_blueprint = False
                character.location = location
                character.save()
                character_form.save_m2m()
                return redirect('npc_cards:location', id=location.id)
                
        elif 'submit_sublocation' in request.POST:
            # Process sublocation form
            sublocation_form = SimpleLocationForm(request.POST)
            if sublocation_form.is_valid():
                sublocation = sublocation_form.save(commit=False)
                sublocation.universe = location.universe  # Inherit universe from parent
                sublocation.parent_location = location
                sublocation.save()
                return redirect('npc_cards:location', id=sublocation.id)
                
        elif 'submit_parent' in request.POST:
            # Process parent location form
            parent_form = SimpleLocationForm(request.POST)
            if parent_form.is_valid():
                parent_location = parent_form.save(commit=False)
                parent_location.universe = location.universe  # Share the same universe
                parent_location.save()
                
                # Set the new location as parent of current
                location.parent_location = parent_location
                location.save()
                return redirect('npc_cards:location', id=parent_location.id)
    
    context = {
        'location': location,
        'item_form': item_form,
        'character_form': character_form,
        'sublocation_form': sublocation_form,
        'parent_form': parent_form,
    }
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
        form = NPCCharacterBlueprintForm(request.POST, request.FILES)
        if form.is_valid():
            blueprint = form.save(commit=False)
            blueprint.is_blueprint = True
            blueprint.save()

            # Save M2M fields
            form.save_m2m()

            return redirect('npc_cards:blueprint_detail', id=blueprint.id)
    else:
        form = NPCCharacterBlueprintForm()

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
                character.creator = request.user
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
            character = form.save(commit=False)
            character.creator = request.user
            character.save()
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
        form = NPCCharacterBlueprintEditForm(request.POST, request.FILES, instance=blueprint)
        if form.is_valid():
            blueprint = form.save(commit=False)
            blueprint.is_blueprint = True
            blueprint.save()
            form.save_m2m()
            return redirect('npc_cards:blueprint_detail', id=blueprint.id)
    else:
        form = NPCCharacterBlueprintEditForm(instance=blueprint)
    
    context = {
        'form':form,
        'blueprint':blueprint,
        'has_instances': NPCCharacter.objects.filter(blueprint=blueprint).exists(),
    }
    return render(request, 'npc_cards/blueprints_edit.html', context=context)

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)


    context = {'item':item}
    return render(request, 'npc_cards/item_detail.html', context=context)