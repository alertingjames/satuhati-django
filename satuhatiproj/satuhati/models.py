from django.db import models

class SatuhatiMember(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    auth_status = models.CharField(max_length=30)
    picture_url = models.CharField(max_length=1000)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)


class Music(models.Model):
    member_id = models.CharField(max_length=11)
    member_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=1000)
    time = models.CharField(max_length=100)
    likes = models.CharField(max_length=11)
    status = models.CharField(max_length=20)
    liked = models.CharField(max_length=20)


class Like(models.Model):
    music_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    liked_time = models.CharField(max_length=50)