from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserFollows(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='followed_user')

    def __str__(self):
        return self.user.username + ' follows ' + self.followed_user.username