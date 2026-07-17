from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):

    class Visibility(models.TextChoices):
        PUBLIC = "PUBLIC", "Public"
        FOLLOWERS = "FOLLOWERS", "Followers"
        PRIVATE = "PRIVATE", "Private"

    class PostType(models.TextChoices):
        POST = "POST", "Post"
        REEL = "REEL", "Reel"
        STORY = "STORY", "Story"
        TEXT = "TEXT", "Text"

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    
    type = models.CharField(
        max_length=10,
        choices=PostType.choices,
        default=PostType.TEXT
    )

    caption = models.TextField(blank=True)
    media = models.FileField(upload_to="posts/",null=True,
    blank=True)

    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PUBLIC
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class PostInteraction(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Like(PostInteraction):
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="like_user_post"
            )
        ]

class Comment(PostInteraction):

    reply_of = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    comment = models.TextField(max_length=520)

class Save(PostInteraction):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="save_user_post"
            )
        ]

class Share(PostInteraction):
    pass

class FeedPriority(models.Model):

    class Priority(models.IntegerChoices):
        NEW = 0, "Never Served"
        SERVED = -1, "Served"
        INTERACTED = -10, "Interacted"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feed_priorities"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="feed_priorities"
    )

    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.NEW
    )

    served_count = models.PositiveIntegerField(default=0)

    last_served_at = models.DateTimeField(
        null=True,
        blank=True
    )

    interacted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="feed_priority_user_post"
            )
        ]

        indexes = [
            models.Index(
                fields=["user", "priority", "last_served_at"]
            )
        ]