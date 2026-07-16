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

    comment = models.TextField(max_length=5200)

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


