from django.db import models


class Articles(models.Model):
    create_data = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500, verbose_name='Title', unique=True)
    text = models.TextField(verbose_name='Text', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

