from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import *
from django.db.models import Q


def competition_list(request):
    competitions = Competition.objects.filter(start_date__lte=timezone.now()).order_by('-start_date')[:20]
    return render(request, 'player/competition_list.html', {'competitions': competitions})


def competition(request, pk):
    current = get_object_or_404(Competition, pk=pk)
    games = Game.objects.filter(competition=current.pk)
    players = []
    for game in games:
        players.append(game.loser)
    players.append(current.winner)
    return render(request, 'player/competition.html', {'competition': current, 'games': games, 'players': players})


def new_competition(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.club = form.cleaned_data['club']
            comp.save()
            return redirect('competition_list')
    else:
        form = CompetitionForm()
    return render(request, 'player/competition_new.html', {'form': form})


def player(request, pk):
    player_ = get_object_or_404(Player, pk=pk)
    recent_games = Game.objects.filter(Q(winner=player_.pk) | Q(loser=player_.pk))
    return render(request, 'player/player.html',
                  {'player': player_, 'recent_games': recent_games})


def player_list(request):
    players = Player.objects.all().order_by('-rating')
    return render(request, 'player/player_list.html', {'players': players})


def new_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.address = form.cleaned_data['address']
            player.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'player/player_new.html', {'form': form})


def new_game(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            if not game.played_date:
                game.played_date = timezone.now()
            game.winner = form.cleaned_data['winner']
            game.loser = form.cleaned_data['loser']
            game.save()
            game.winner.rating = game.winner.rating + 10
            game.winner.save()
            game.loser.rating = game.loser.rating - 10
            game.loser.save()
            return redirect('game_list')
    else:
        form = GameForm()
    return render(request, 'player/game_new.html', {'form': form})


def game_list(request):
    games = Game.objects.all().order_by('-played_date')[:20]
    return render(request, 'player/game_list.html', {'games': games})


def club_list(request):
    clubs = BilliardClub.objects.all()
    return render(request, 'player/club_list.html', {'clubs': clubs})


def club_detail(request, pk):
    club = get_object_or_404(BilliardClub, pk=pk)
    competitions = Competition.objects.filter(club=club)
    return render(request, 'player/club.html', {'club': club, 'competitions': competitions})


def player_search(request, name):
    players = Player.objects.filter(name__contains=name).order_by('-rating')
    return render(request, 'player/player_list.html', {'players': players})
