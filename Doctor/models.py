from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False)
    cpf = models.CharField(max_length=11, null=False, unique=True)
    rg = models.CharField(max_length=9, null=False, unique=True)
    email = models.EmailField(unique=True, max_length=150)
    crm = models.CharField(max_length=6, null=False, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


