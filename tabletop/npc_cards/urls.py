from django.urls import path
from .views import index, NPCCharacterCardsView, UniverseView, LocationDetailView

urlpatterns = [
    path('', index),
    path('npc_cards/', NPCCharacterCardsView),
    path('universes/', UniverseView),
    path('location/<int:id>/', LocationDetailView),
]