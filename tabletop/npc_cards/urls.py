from django.urls import path
from .views import index, NPCCharacterCardsView, UniverseView

urlpatterns = [
    path('', index),
    path('npc_cards/', NPCCharacterCardsView),
    path('universes/', UniverseView),
]