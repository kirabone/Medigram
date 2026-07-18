from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from ..models import Comment
from Post.services.show import PostShow


COMMENT_CACHE = {}


class CommentShow:

    PAGE_SIZE = 10

    @staticmethod
    def comments(user, post_id, offset=0):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        PostShow.can_interact(user, post)

        if post_id not in COMMENT_CACHE:
            COMMENT_CACHE[post_id] = {}

        if offset not in COMMENT_CACHE[post_id]:

            COMMENT_CACHE[post_id][offset] = list(
                Comment.objects.filter(
                    post=post
                )
                .select_related("user")
                .prefetch_related(
                    "likes",
                    "replies"
                )
                .order_by("created_at")[offset:offset + CommentShow.PAGE_SIZE]
            )

        return COMMENT_CACHE[post_id][offset]