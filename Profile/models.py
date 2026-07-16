from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    class AccountType(models.TextChoices):
        PRIVATE = 'PRIVATE' , 'private'
        PUBLIC = 'PUBLIC' , 'public'

    user = models.OneToOneField(User, on_delete=models.CASCADE )

    account_type = models.CharField(
        choices = AccountType.choices,
        default=AccountType.PUBLIC
    )

    bio = models.TextField(max_length=120)

    bdate = models.DateField(default=None, 
                             null=True,
                             black=True)
