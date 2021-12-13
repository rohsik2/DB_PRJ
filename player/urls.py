from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('competitions', views.competition_list, name='competition_list'),
    path('competitions/<int:pk>', views.competition, name='competition_detail'),
    path('competitions/new', views.new_competition, name='new_competition'),

    path('player', views.player_list, name='player_list'),
    path('player/<int:pk>', views.player, name='player_detail'),
    path('player/new', views.new_player, name='new_player'),
    path('player/search/<str:name>', views.player_search, name='search_player'),
    path('game', views.game_list, name='game_list'),
    path('game/new', views.new_game, name='new_game'),

    path('club', views.club_list, name="club_list"),
    path('club/<int:pk>', views.club_detail, name="club_detail"),

    path('', views.competition_list),
]