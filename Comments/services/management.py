from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from ..models import (
    Comment,
    CommentHeart,
    PinnedComment,
)


class CommentManagement:

    @staticmethod
    def pin(user, comment_id):

        comment = get_object_or_404(
            Comment,
            id=comment_id
        )

        if comment.post.uploader != user:
            raise PermissionDenied()

        if PinnedComment.objects.filter(
            comment__post=comment.post
        ).count() >= 3:
            raise PermissionDenied("Maximum pinned comments reached.")

        PinnedComment.objects.get_or_create(
            comment=comment,
            pinned_by=user
        )

    @staticmethod
    def unpin(user, comment_id):

        comment = get_object_or_404(
            Comment,
            id=comment_id
        )

        if comment.post.uploader != user:
            raise PermissionDenied()

        PinnedComment.objects.filter(
            comment=comment
        ).delete()

    @staticmethod
    def heart(user, comment_id):

        comment = get_object_or_404(
            Comment,
            id=comment_id
        )

        if comment.post.uploader != user:
            raise PermissionDenied()

        CommentHeart.objects.update_or_create(
            comment=comment,
            defaults={
                "hearted_by": user
            }
        )

    @staticmethod
    def unheart(user, comment_id):

        comment = get_object_or_404(
            Comment,
            id=comment_id
        )

        if comment.post.uploader != user:
            raise PermissionDenied()

        CommentHeart.objects.filter(
            comment=comment
        ).delete()