from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Userstable(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Roles(models.Model):
    role_names = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_names


class UserRole(models.Model):
    user = models.ForeignKey(Userstable, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='role_users')

    def __str__(self):
        return f"{self.user.username} - {self.role.role_names}"

