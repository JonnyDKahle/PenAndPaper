from django.shortcuts import render, get_object_or_404, redirect
from .models import NPCCharacter, Universe, Location, Item
from .forms import LocationForm, NPCCharacterForm, NPCCharacterFormBlueprintForm, NPCCharacterBlueprintEditForm
from .forms import NPCCharacterBlueprintForm, ItemCreateForm, SimpleLocationForm, MapLocationForm
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

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
    map_location_form = MapLocationForm()
    parent_form = SimpleLocationForm()

    # Get mapped sub-locations
    mapped_sublocations = location.sub_locations.exclude(x_coord__isnull=True).exclude(y_coord__isnull=True)
    
    # Prepare sublocations data for JavaScript
    mapped_sublocations_data = []
    for sublocation in mapped_sublocations:
        mapped_sublocations_data.append({
            'id': sublocation.id,
            'name': sublocation.name,
            'x_coord': float(sublocation.x_coord),
            'y_coord': float(sublocation.y_coord)
        })
    
    if request.method == 'POST':
        if 'upload_map' in request.POST:
            if 'location_image' in request.FILES:
                location.image = request.FILES['location_image']
                location.save()
                return redirect('npc_cards:location', id=location.id)
    
        if 'submit_map_location' in request.POST:
            # Process map-based location creation
            map_location_form = MapLocationForm(request.POST)
            if map_location_form.is_valid():
                sublocation = map_location_form.save(commit=False)
                sublocation.universe = location.universe
                sublocation.parent_location = location
                sublocation.creator = request.user
                sublocation.x_coord = map_location_form.cleaned_data['x_coord']
                sublocation.y_coord = map_location_form.cleaned_data['y_coord']
                sublocation.save()
                return redirect('npc_cards:location', id=location.id)

        elif 'submit_item' in request.POST:
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
        'map_location_form': map_location_form,
        'parent_form': parent_form,
        'mapped_sublocations': mapped_sublocations,
        'mapped_sublocations_json': json.dumps(mapped_sublocations_data, cls=DjangoJSONEncoder),
    }
    return render(request, 'npc_cards/location_detail.html', context=context)

def location_edit(request, id):
    location = get_object_or_404(Location, id=id)
    
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=location)
        if form.is_valid():
            form.save()
            return redirect('npc_cards:location', id=location.id)
    else:
        form = LocationForm(instance=location)
    
    context = {
        'form': form,
        'location': location,
    }
    return render(request, 'npc_cards/location_edit.html', context=context)

@login_required
def location_delete(request, id):
    location = get_object_or_404(Location, id=id)
    parent_id = None
    
    if location.parent_location:
        parent_id = location.parent_location.id
    
    # Get return location ID from form if provided
    if request.method == 'POST':
        return_to = request.POST.get('return_to')
        if return_to:
            try:
                return_to_id = int(return_to)
                if Location.objects.filter(id=return_to_id).exists():
                    parent_id = return_to_id
            except:
                pass
        
        location.delete()
        
        if parent_id:
            return redirect('npc_cards:location', id=parent_id)
        else:
            return redirect('npc_cards:index')
    
    return redirect('npc_cards:location', id=id)

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

@login_required
def delete_character(request, id):
    character = get_object_or_404(NPCCharacter, id=id)
    location_id = None

    if character.location:
        location_id = character.location.id

    if request.method == 'POST':
        character.delete()
        if location_id:
            return redirect('npc_cards:location', id=location_id)
        else:
            return redirect('npc_cards:character_list')
        
    return redirect('npc_cards:character_detail', id=id)

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

def item_edit(request, id):
    item = get_object_or_404(Item, id=id)
    
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('npc_cards:item_detail', id=item.id)
    else:
        form = ItemCreateForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'npc_cards/item_edit.html', context=context)

def item_delete(request, id):
    item = get_object_or_404(Item, id=id)
    location = None
    
    # Find a location that has this item to redirect back to
    for loc in Location.objects.filter(items=item):
        location = loc
        break
    
    if request.method == 'POST':
        # Remove the item from all locations
        for loc in Location.objects.filter(items=item):
            loc.items.remove(item)
        
        # Delete the item
        item.delete()
        
        # Redirect back to the location if we found one
        if location:
            return redirect('npc_cards:location', id=location.id)
        else:
            return redirect('npc_cards:index')
    
    return redirect('npc_cards:item_detail', id=id)

@require_POST
def update_character_stat(request, character_id):
    # Get the character
    character = get_object_or_404(NPCCharacter, id=character_id)
    
    try:
        # Parse JSON data
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')
        
        # Validate field name to prevent potential security issues
        allowed_fields = [
            'strength', 'dexterity', 'constitution', 
            'intelligence', 'wisdom', 'charisma',
            'armor_class', 'health_points', 'speed',
            'notes'
        ]
        
        if field not in allowed_fields:
            return JsonResponse({'success': False, 'error': 'Invalid field'})
        
        # Update the field
        setattr(character, field, value)
        character.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})