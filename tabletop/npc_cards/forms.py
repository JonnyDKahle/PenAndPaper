from django import forms
from .models import Location, NPCCharacterCard, NPCInstance

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class NPCInstanceForm(forms.ModelForm):
    class Meta:
        model = NPCInstance
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'character_card' in self.data and self.data['character_card']:
    #         try:
    #             character_id = self.data['character_card']
    #             character = NPCCharacterCard.objects.get(id=character_id)
