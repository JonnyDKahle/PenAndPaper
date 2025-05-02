from django.contrib import admin
from .models import NPCCharacterCard, Skill, DamageResistance, Sense

# Register your models here.
admin.site.register(NPCCharacterCard)
admin.site.register(Skill)
admin.site.register(DamageResistance)
admin.site.register(Sense)