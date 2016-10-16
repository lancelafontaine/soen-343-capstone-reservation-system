from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Reservation(models.Model):
    he = 2
    # start_time
    # end_time
    # user_id
    # room_number

class Room(models.Model):
    df = 3
    # number

class WaitingList(models.Model):
    d = 3
    # Linked to many reservations