from django.db import models


class User_tokens(models.Model):
    name = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    state_key = models.CharField(max_length=100)


    def __str__(self):
        return self.name
