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
                             blank=True)

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow"
            )
        ]

class FollowRequest(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_follow_requests"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_follow_requests"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_follow_request"
            )
        ]

class Block(models.Model):

    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocking"
    )

    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocked_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["blocker", "blocked"],
                name="unique_block"
            )
        ]


    

    