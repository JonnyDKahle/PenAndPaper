from django import forms
from .models import Location, NPCCharacter

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class NPCCharacterForm(forms.ModelForm):
    """Form for creating/editing a character"""
    class Meta:
        model = NPCCharacter
        exclude = ['is_blueprint', 'blueprint']
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
