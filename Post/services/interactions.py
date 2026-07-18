from ..models import Post, Like, Save
from django.shortcuts import get_object_or_404
from django.utils import timezone
from Profile.models import Block
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from Profile.models import Follow

class PostInteractions:

    @staticmethod
    def like_post(user, post_id):

        post = get_object_or_404(Post, id=post_id)

        if Block.objects.filter(
            Q(blocker=user, blocked=post.uploader) |
            Q(blocker=post.uploader, blocked=user)
        ).exists():
            raise PermissionDenied("You cannot interact with this post.")

        like, created = Like.objects.get_or_create(
            user=user,
            post=post
        )

        return like
    
    @staticmethod
    def unlike_post(user, post_id):

        Like.objects.filter(
            user=user,
            post_id=post_id
        ).delete()

    @staticmethod
    def save_post(user, post_id):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        PostInteractions.can_interact(
            user,
            post
        )

        save, created = Save.objects.get_or_create(
            user=user,
            post=post
        )

        return save
    
    @staticmethod
    def unsave_post(user, post_id):

        Save.objects.filter(
            user=user,
            post_id=post_id
        ).delete()
