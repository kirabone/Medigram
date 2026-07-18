from ..models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone
from Profile.models import Block
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from Profile.models import Follow

class PostShow:
    @staticmethod
    def can_interact(user, post):

        # Deleted post
        if post.deleted_at is not None:
            raise PermissionDenied("This post no longer exists.")

        # Block check
        if Block.objects.filter(
            Q(blocker=user, blocked=post.uploader) |
            Q(blocker=post.uploader, blocked=user)
        ).exists():
            raise PermissionDenied("You cannot interact with this post.")

        # Visibility check
        if post.visibility == Post.Visibility.PRIVATE:
            raise PermissionDenied("This post is private.")

        if (
            post.visibility == Post.Visibility.FOLLOWERS and
            not Follow.objects.filter(
                follower=user,
                following=post.uploader
            ).exists()
        ):
            raise PermissionDenied(
                "You must follow this user."
            )



    @staticmethod
    def saved_posts(user):

        return Post.objects.filter(
            save__user=user,
            deleted_at__isnull=True
        ).exclude(
            Q(uploader__blocking__blocked=user) |
            Q(uploader__blocked_by__blocker=user)
        ).order_by("-created_at")
    
    @staticmethod
    def generate_feed(user, post_types):

        # Never include stories in the normal feed
        allowed_types = [
            post_type
            for post_type in post_types
            if post_type != Post.PostType.STORY
        ]

        queryset = Post.objects.filter(
            deleted_at__isnull=True,
            type__in=allowed_types
        )

        # Remove blocked users (both directions)
        queryset = queryset.exclude(
            Q(uploader__blocking__blocked=user) |
            Q(uploader__blocked_by__blocker=user)
        )

        # Get people the user follows
        following = Follow.objects.filter(
            follower=user
        ).values_list(
            "following_id",
            flat=True
        )

        # Visibility rules
        queryset = queryset.filter(
            Q(visibility=Post.Visibility.PUBLIC) |
            Q(
                visibility=Post.Visibility.FOLLOWERS,
                uploader_id__in=following
            )
        )

        # Random order
        return queryset.order_by("?")
