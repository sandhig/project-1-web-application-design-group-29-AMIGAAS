from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.user.email

    def generate_verification_code(self):
        code = get_random_string(6, '0123456789')
        self.verification_code = code
        self.save()
        return code
