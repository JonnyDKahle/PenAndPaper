from django.urls import path
from . import views

app_name = 'npc_cards'
urlpatterns = [
    path('', views.index, name='index'),
    # path('npc_cards/', NPCCharacterCardsView),
    path('universes/', views.UniverseView, name='universes'),
    path('location/<int:id>/', views.LocationDetailView, name='location'),
    path('location/<int:id>/edit/', views.location_edit, name='location_edit'),
    path('location/<int:id>/delete/', views.location_delete, name='location_delete'),
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
    path('character/<int:id>/delete/', views.delete_character, name='character_delete'),
    path('character/<int:character_id>/update-stat/', views.update_character_stat, name='update_character_stat'),

    # Item URLs
    # path('location/<int:location_id>/items/create', views.create_item, name='create_item'),
    # path('items/create', views.create_item, name='create_item'),
    path('items/<int:id>/', views.item_detail, name='item_detail'),
    path('item/<int:id>/edit/', views.item_edit, name='item_edit'),
    path('item/<int:id>/delete/', views.item_delete, name='item_delete'),
]