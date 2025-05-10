from django import forms
from .models import Location, NPCCharacter, Item

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class SimpleLocationForm(forms.ModelForm):
    """Simplified form for creating locations from location detail page"""
    class Meta:
        model = Location
        fields = ['name', 'story']
        widgets = {
            'story': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief description of this location'}),
        }

class NPCCharacterForm(forms.ModelForm):
    """Form for creating/editing a character"""
    class Meta:
        model = NPCCharacter
        exclude = ['is_blueprint', 'blueprint']
        widgets = {
            'race':forms.Select(),
            'alignment':forms.Select(),
            }
        
class NPCCharacterBlueprintForm(forms.ModelForm):
    """Form for creating/editing a character"""
    class Meta:
        model = NPCCharacter
        exclude = ['is_blueprint', 'blueprint', 'location']
        widgets = {
            'race':forms.Select(),
            'alignment':forms.Select(),
            }
        
class NPCCharacterFormBlueprintForm(forms.Form):
    """Form for creating a character from a blueprint"""
    blueprint = forms.ModelChoiceField(
        queryset = NPCCharacter.objects.filter(is_blueprint=True),
        label="Blueprint"
    )
    name = forms.CharField(max_length=100, required=False, help_text="Leave blank to use blueprint name")
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        required=False
    )
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     del self.fields['location']

class NPCCharacterBlueprintEditForm(forms.ModelForm):
    """Form for editing a NPC blueprint"""
    class Meta:
        model = NPCCharacter
        exclude = ['is_blueprint', 'blueprint', 'location']
        widgets = {
            'race':forms.Select(),
            'alignment':forms.Select(),
        }

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
