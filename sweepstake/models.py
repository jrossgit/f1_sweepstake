from django.db import models
from django.contrib import admin

class Team(models.Model):

    name = models.CharField(max_length=30)
    colour = models.CharField(max_length=7)  # Hex code string, e.g. '#ff0000'
    active = models.BooleanField(default=True)

    def __str__(self):
        return '<Team: {}>'.format(self.name)


class Driver(models.Model):

    name = models.CharField(max_length=30)
    team = models.ForeignKey(Team, related_name='drivers')

    def __str__(self):
        return '<Driver: {}>'.format(self.name)


admin.site.register(Team)
admin.site.register(Driver)
