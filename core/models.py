from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
