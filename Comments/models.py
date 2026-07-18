from django.db import models
from Post.models import PostInteraction
from django.contrib.auth.models import User

class Comment(PostInteraction):

    reply_of = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    comment = models.TextField(max_length=520)

class CommentLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="liked_comments"
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="unique_comment_like"
            )
        ]

class CommentHeart(models.Model):
    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        related_name="heart"
    )

    hearted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hearted_comments"
    )

    created_at = models.DateTimeField(auto_now_add=True)

class PinnedComment(models.Model):
    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        related_name="pin"
    )

    pinned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pinned_comments"
    )

    created_at = models.DateTimeField(auto_now_add=True)