from django.contrib import admin
from .models import NPCCharacter, Skill, DamageResistance, Sense, Universe, Location, Item

# Register your models here.
admin.site.register(NPCCharacter)
admin.site.register(Skill)
admin.site.register(DamageResistance)
admin.site.register(Sense)
admin.site.register(Universe)
admin.site.register(Location)
admin.site.register(Item)