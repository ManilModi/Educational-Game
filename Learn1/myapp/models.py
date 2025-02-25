from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# User Model (Basic User Info Only)
class Userstable(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Storing hashed passwords

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

# Predefined Roles Model
class Roles(models.Model):
    role_names = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_names

# UserRole Model (Junction Table for User-Role Mapping)
class UserRole(models.Model):
    user = models.ForeignKey(Userstable, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='role_users')

    def __str__(self):
        return f"{self.user.username} - {self.role.role_names}"

# class Institute:
#     pass

# class NormalUser(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)

#     def __str__(self):
#         return self.username


# class Entrepreneur(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)
#     company_name = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return self.username


# class GovernmentEngineer(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)
#     department = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return self.username


# class Researcher(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)
#     institution = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return self.username


# class Admin(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)
#     access_level = models.IntegerField(default=1)

#     def __str__(self):
#         return self.username