from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from ..models import Comment, CommentLike
from Post.services.show import PostShow


class CommentInteractions:

    @staticmethod
    def like(user, comment_id):

        comment = get_object_or_404(Comment, id=comment_id)

        PostShow.can_interact(user, comment.post)

        CommentLike.objects.get_or_create(
            user=user,
            comment=comment
        )

    @staticmethod
    def unlike(user, comment_id):

        comment = get_object_or_404(Comment, id=comment_id)

        CommentLike.objects.filter(
            user=user,
            comment=comment
        ).delete()

