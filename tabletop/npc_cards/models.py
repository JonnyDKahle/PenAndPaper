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
    def __str__(self):
        return self.name
    
class NPCInstance(NPCCharacterCard):
    Name = models.CharField(max_length=100, default="NPC")
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='location_npc')
    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class DamageResistance(models.Model):
    name = models.CharField(max_length=100)
    fraction = models.FloatField(help_text='Fraction of damage taken, e.g., 0.25 for 25% damage taken.')
    def __str__(self):
        return self.name

class Sense(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name



class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class Universe(models.Model):
    name = models.CharField(max_length=100)
    # FK to the GameMaster (Who is just a user)
    def __str__(self):
        return self.name
    
class Location(models.Model): # has: npcs, items # is part of: universe
    name = models.CharField(max_length=100)
    story = models.TextField(null=True, blank=True)
    secret = models.TextField(blank=True, null=True)
    universe = models.ForeignKey('Universe', on_delete=models.CASCADE)
    parent_location = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_locations')
    # npcs, ManyToOne trough FK in NPCInstance
    items = models.ManyToManyField('Item', blank=True, null=True)
    def __str__(self):
        return self.name