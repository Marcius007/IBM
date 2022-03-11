from django.db import models
from django.contrib.auth.models import User


class UserGifs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    search_text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)


class GifLinks(models.Model):
    user_gif_id = models.ForeignKey(UserGifs, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    gif_address = models.TextField()