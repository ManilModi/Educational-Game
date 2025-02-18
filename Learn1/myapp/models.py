from django.db import models


class Users(models.Model):
    
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('entrepreneur', 'Entrepreneur'),
        ('researcher', 'Researcher'),
        ('govt. engineer', 'Government Engineer'),
        ('admin', 'Admin')
    ]
    
    user_id=models.IntegerField(max_length=1000)
    role=models.CharField(choices=USER_TYPE_CHOICES, max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username


class Roles(models.Model):
    role_id=models.IntegerField(max_length=5)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    role_names=models.CharField(max_length=50)

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
