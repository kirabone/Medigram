from ..models import Comment
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


class CommentLifeCycle:

    @staticmethod
    def comment_post(user, post_id, validated_data, reply_of_id=None):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        reply_of = None

        if reply_of_id is not None:
            reply_of = get_object_or_404(
                Comment,
                id=reply_of_id,
                post=post
            )

        return Comment.objects.create(
            user=user,
            post=post,
            reply_of=reply_of,
            **validated_data
        )
    
    @staticmethod
    def delete_comment(user, comment_id):

        comment = get_object_or_404(
            Comment,
            id=comment_id
        )

        if (
            comment.user != user and
            comment.post.uploader != user
        ):
            raise PermissionDenied()

        comment.delete()

        return comment
    
    