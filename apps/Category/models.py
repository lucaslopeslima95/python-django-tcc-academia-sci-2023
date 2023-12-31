from django.db import models

class Category(models.Model):
    name = models.CharField(unique=True,max_length=99,default="Nome Categoria")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name