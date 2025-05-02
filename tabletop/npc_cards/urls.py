from django.urls import path
from .views import index, NPCCharacterCardsView

urlpatterns = [
    path('', index),
    path('npc_cards', NPCCharacterCardsView),
]