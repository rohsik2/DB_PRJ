from django import forms
from .models import *
from django.forms import modelformset_factory
from django.forms import formset_factory


class CompetitionForm(forms.ModelForm):
    club = forms.ModelChoiceField(queryset=BilliardClub.objects.all())

    class Meta:
        model = Competition
        fields = {'name', 'start_date'}


class GameForm(forms.ModelForm):
    winner = forms.ModelChoiceField(queryset=Player.objects.all())  # Or whatever query you'd like
    loser = forms.ModelChoiceField(queryset=Player.objects.all())  # Or whatever query you'd like

    class Meta:
        model = Game
        fields = {'played_date', 'competition'}


class PlayerForm(forms.ModelForm):
    address = forms.ModelChoiceField(queryset=Address.objects.all())

    class Meta:
        model = Player
        fields = {'name', 'age'}