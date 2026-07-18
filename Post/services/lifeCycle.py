from ..models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone
from Profile.models import Block
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from Profile.models import Follow

class PostLifeCycle:

    @staticmethod
    def create_post(user, validated_data):
        return Post.objects.create(
            uploader=user,
            **validated_data
        )
    
    @staticmethod
    def delete_post(user, post_id):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        if post.uploader != user:
            return None

        post.deleted_at = timezone.now()
        post.save(update_fields=["deleted_at"])

        return post
    
    @staticmethod
    def update_post(user, post_id, caption):    

        post = get_object_or_404(
            Post,
            id=post_id,
            deleted_at__isnull=True
        )

        if post.uploader != user:
            raise PermissionDenied()

        post.caption = caption
        post.save(update_fields=["caption"])

        return post
    