from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=100 ,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=80)
    is_premium = models.BooleanField(default=False),
    is_anonymous = models.BooleanField(default=False),
    is_authenticated = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS=["email"]

    def __str__(self):
        return self.username