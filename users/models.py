from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager

class UserRole(models.Model):
    """
    Maintains roles available in the system
    """
    class Meta:
        db_table = 'user_role'
    name = models.CharField(max_length=20)

class UserManager(BaseUserManager):
    """
    Manage user creation
    """

    def create_user(self, email, password=None, **extra_fields):
        # Default email isn't verified. To get it verified via email link
        user = self.model(email=email, is_email_verified=False, **extra_fields)

        user.set_password(password)
        user.save()

        return user

class Users(AbstractBaseUser):
    """
    Stores User detail
    """
    first_name = models.CharField(max_length=120)

    last_name = models.CharField(max_length=120)

    email = models.EmailField(unique=True)

    is_email_verified = models.BooleanField(default=False)

    # password = models.CharField(max_length=128)

    organization = models.CharField(max_length=120)

    contact_no = models.CharField(max_length=10)

    address = models.TextField()

    objects = UserManager()

    created = models.DateTimeField(auto_now_add=True)  # Registration date

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

class TokenList(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    token = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'token_list'
