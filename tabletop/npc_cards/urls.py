from django.urls import path
from . import views

app_name = 'npc_cards'
urlpatterns = [
    path('', views.index),
    # path('npc_cards/', NPCCharacterCardsView),
    path('universes/', views.UniverseView, name='universes'),
    path('location/<int:id>/', views.LocationDetailView, name='location'),
    # path('create_npcinstance/', CreateNPCInstaceView, name='create_npcinstance'),

    # Character & Blueprint URLs
    path('blueprints/', views.blueprint_list, name='blueprint_list'),
    path('blueprints/create/', views.create_blueprint, name='create_blueprint'),
    path('blueprints/<int:id>/', views.character_detail, name='blueprint_detail'),
    path('blueprints/<int:id>/edit/', views.edit_blueprint, name='edit_blueprint'),

    path('characters/', views.character_list, name='character_list'),
    path('characters/create/', views.create_character, name='create_character'),
    path('characters/<int:id>/', views.character_detail, name='character_detail'),
    path('characters/<int:id>/edit/', views.edit_character, name='edit_character'),
]