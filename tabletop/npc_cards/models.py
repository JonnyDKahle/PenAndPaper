from django.db import models

# Create your models here.
class NPCCharacterCard(models.Model):
    # Character Attributes:
    image_url = models.ImageField(upload_to='npc_cards/', blank=True)
    name = models.CharField(max_length=100)
    RACE_CHOICES = [
        ('human', 'Human'),
        ('elf', 'Elf'),
        ('dwarf', 'Dwarf'),
        ('halfling', 'Halfling'),
        ('orc', 'Orc'),
        ('tiefling', 'Tiefling'),
        ('dragonborn', 'Dragonborn'),
        ('gnome', 'Gnome'),
    ]
    race = models.CharField(max_length=50, choices=RACE_CHOICES, blank=True)
    ALIGNMENT_CHOICES = [
        ('lg', 'Lawful Good'),
        ('ng', 'Neutral Good'),
        ('cg', 'Chaotic Good'),
        ('ln', 'Lawful Neutral'),
        ('tn', 'True Neutral'),
        ('cn', 'Chaotic Neutral'),
        ('le', 'Lawful Evil'),
        ('ne', 'Neutral Evil'),
        ('ce', 'Chaotic Evil'),
    ]
    alignment = models.CharField(max_length=50, choices=ALIGNMENT_CHOICES, blank=True)
    armor_class = models.IntegerField()
    health_points = models.IntegerField()
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()
    speed = models.IntegerField()
    challange_rating = models.FloatField()
    xp_gain = models.IntegerField()

    # ManyToManyFields
    skills = models.ManyToManyField('Skill', related_name='npc_cards_skills', blank=True)
    damage_resistances = models.ManyToManyField('DamageResistance', related_name='npc_cards_damage_resistances', blank=True)
    senses = models.ManyToManyField('Sense', related_name='npc_cards_senses', blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class DamageResistance(models.Model):
    name = models.CharField(max_length=100)
    fraction = models.FloatField(help_text='Fraction of damage taken, e.g., 0.25 for 25% damage taken.')

class Sense(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class NPCCharacterCardBorrowed(NPCCharacterCard):
    pass