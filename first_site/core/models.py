from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author of article', blank = True, null = True)
    create_data = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500, verbose_name='Title', unique=True)
    text = models.TextField(verbose_name='Text', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

