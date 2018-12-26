from django.db import models
from django.shortcuts import render, reverse

class Book(models.Model):
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')

    def __str__(self):
        return self.my_field_name

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])



class Article(models.Model):
    title = models.CharField(max_length=120)
    content= models.TextField()
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("features:article-detail", kwargs={"id": self.id})


