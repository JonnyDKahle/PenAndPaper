from django.db import models

# Create your models here.
class NPCCharacter(models.Model):
    # Blueprint Attributes
    is_blueprint = models.BooleanField(default=False)
    blueprint = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='instances', null=True, blank=True)

    # Character Attributes:
    image_url = models.ImageField(upload_to='npc_cards/', blank=True)
    name = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)

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
    race = models.CharField(max_length=50, choices=RACE_CHOICES, default='human', blank=True, null=True)

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
    alignment = models.CharField(max_length=50, choices=ALIGNMENT_CHOICES, blank=True, null=True)

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

    # Location - only for instances, not blueprints
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='npcs', null=True, blank=True)

    # ManyToManyFields
    skills = models.ManyToManyField('Skill', related_name='npc_cards_skills', blank=True)
    damage_resistances = models.ManyToManyField('DamageResistance', related_name='npc_cards_damage_resistances', blank=True)
    senses = models.ManyToManyField('Sense', related_name='npc_cards_senses', blank=True)

    def __str__(self):
        if self.is_blueprint:
            return f"[Blueprint] {self.name}"
        return f"{self.name}"
    
    def create_instance(self, instance_name=None, location=None): # Check - If creating on a location, location should be the specific location
        """Create a new character instance based on this blueprint"""
        if not self.is_blueprint: # Amend - Instances should be able to be replicated
            raise ValueError("Only blueprints can be used to create instances")
        
        instance = NPCCharacter.objects.create(
            is_blueprint=False,
            blueprint=self,
            name=instance_name or self.name, # Amend - Differentiate between name of class and name of character
            race=self.race, # Amend - there is no race attribute set to a blueprint
            alignment=self.alignment, # Amend - there is no alignment attribute set to a blueprint
            armor_class=self.armor_class,
            health_points=self.health_points,
            strength=self.strength,
            dexterity=self.dexterity,
            constitution=self.constitution,
            intelligence=self.intelligence,
            wisdom=self.wisdom,
            charisma=self.charisma,
            speed=self.speed,
            challange_rating=self.challange_rating,
            xp_gain=self.xp_gain,
            location=location
        )

        # Copy M2M relationships
        for skill in self.skills.all():
            instance.skills.add(skill)

        for resistance in self.damage_resistances.all():
            instance.damage_resistances.add(resistance)

        for sense in self.senses.all():
            instance.senses.add(sense)

        return instance
    

    



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
    universe = models.ForeignKey('Universe', on_delete=models.CASCADE, related_name='locations', null=True)
    parent_location = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_locations')
    # npcs, ManyToOne trough FK in NPCInstance
    items = models.ManyToManyField('Item', blank=True)
    def __str__(self):
        return self.name