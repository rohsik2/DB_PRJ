from django.db import models


class Address(models.Model):
    do_name = models.CharField(max_length=30)
    si_name = models.CharField(max_length=30)
    gu_name = models.CharField(max_length=30)
    dong_name = models.CharField(max_length=30)

    def __str__(self):
        return self.do_name + ' ' + self.si_name + ' ' + self.gu_name + ' ' + self.dong_name


class BilliardClub(models.Model):
    open_date = models.DateTimeField()
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=30)
    rating = models.IntegerField(default=1000)
    age = models.IntegerField(default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=100, default="")
    start_date = models.DateTimeField()
    club = models.ForeignKey(BilliardClub, on_delete=models.SET_NULL, null=True)
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    played_date = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='loser')
    loser = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='winner')
    average_rating = models.IntegerField(default=-1)
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.winner.name + ' ' + self.loser.name

    def save(self, *args, **kwargs):
        if self.average_rating == -1:
            self.average_rating = (self.winner.rating + self.loser.rating) // 2
            self.save(*args, **kwargs)
        super().save(*args, **kwargs)
