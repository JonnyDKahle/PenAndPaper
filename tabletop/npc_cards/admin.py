from django.contrib import admin
from .models import NPCCharacterCard, Skill, DamageResistance, Sense, Universe, Location, NPCInstance, Item

# Register your models here.
admin.site.register(NPCCharacterCard)
admin.site.register(Skill)
admin.site.register(DamageResistance)
admin.site.register(Sense)
admin.site.register(Universe)
admin.site.register(Location)
admin.site.register(NPCInstance)
admin.site.register(Item)