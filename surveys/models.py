from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    def is_valid(self):
        pass


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    deadline = models.DateField(null=True)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    def is_valid(self):
        pass


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_id(self):
        return self.id

    def is_valid(self):
        pass


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number_of_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def get_id(self):
        return self.id

    def is_valid(self):
        pass


class Response(models.Model):
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)


class UserCategorySubscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


