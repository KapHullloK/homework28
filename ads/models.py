from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    role = models.CharField(max_length=20)
    age = models.IntegerField()
    location_id = models.IntegerField()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']


class Ad(models.Model):
    name = models.CharField(max_length=130)
    author_id = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=2500)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    category_id = models.IntegerField()

    def __str__(self):
        return self.name
