from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=False, default="")
    created_at = models.DateField(auto_now_add=True)

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True, default="")

class Authors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)


