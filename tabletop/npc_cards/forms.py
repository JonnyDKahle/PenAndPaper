from django import forms
from .models import Location, NPCCharacter

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

