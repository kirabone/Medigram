from .models import Post, Like, Comment, Save
from django.shortcuts import get_object_or_404
from django.utils import timezone

class PostService:

    @staticmethod
    def create_post(user, validated_data):
        return Post.objects.create(
            uploader=user,
            **validated_data
        )
    
    @staticmethod
    def get_post(post_id):
        return get_object_or_404(
            Post,
            id=post_id
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
    def like_post(user, post_id):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        like, created = Like.objects.get_or_create(
            user=user,
            post=post
        )

        return like
    
    @staticmethod
    def unlike_post(user, post_id):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        like = get_object_or_404(
            Like,
            user=user,
            post=post
        )

        like.delete()

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

        if comment.user != user:
            return None

        comment.delete()

        return comment
    
    @staticmethod
    def save_post(user, post_id):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        save, created = Save.objects.get_or_create(
            user=user,
            post=post
        )

        return save

    @staticmethod
    def unsave_post(user, post_id):

        save = get_object_or_404(
            Save,
            user=user,
            post_id=post_id
        )

        save.delete()

    @staticmethod
    def feed_posts():

        return Post.objects.filter(
            type__in=[
                Post.PostType.POST,
                Post.PostType.TEXT
            ],
            visibility=Post.Visibility.PUBLIC,
            deleted_at__isnull=True
        ).order_by("-created_at")


    @staticmethod
    def feed_reels():

        return Post.objects.filter(
            type=Post.PostType.REEL,
            visibility=Post.Visibility.PUBLIC,
            deleted_at__isnull=True
        ).order_by("-created_at")


    @staticmethod
    def profile_posts(user_id):

        return Post.objects.filter(
            uploader_id=user_id,
            type=Post.PostType.POST,
            deleted_at__isnull=True
        ).order_by("-created_at")


    @staticmethod
    def profile_reels(user_id):

        return Post.objects.filter(
            uploader_id=user_id,
            type=Post.PostType.REEL,
            deleted_at__isnull=True
        ).order_by("-created_at")


    @staticmethod
    def profile_texts(user_id):

        return Post.objects.filter(
            uploader_id=user_id,
            type=Post.PostType.TEXT,
            deleted_at__isnull=True
        ).order_by("-created_at")


    @staticmethod
    def saved_posts(user):

        return Post.objects.filter(
            save__user=user,
            deleted_at__isnull=True
        ).order_by("-created_at")
    
import random

from django.db import transaction
from django.utils import timezone

from .models import FeedPriority


class FeedService:

    FEED_SIZE = 5

    @classmethod
    def get_feed(cls, user, types):

        candidates = cls._load_candidates(user, types)

        return cls._select_posts(candidates)

    @classmethod
    def _load_candidates(cls, user, types):
        """
        Loads every post the user is allowed to see.
        """

        return list(

            Post.objects.filter(

                type__in=types

            ).select_related(

                "uploader"

            ).order_by(

                "-created_at"

            )[:100]

        )

    @classmethod
    def _select_posts(cls, candidates):
        """
        Temporary V1 selector.

        Later this becomes FeedPriority ranking.
        """

        if len(candidates) <= cls.FEED_SIZE:
            return candidates

        return random.sample(
            candidates,
            cls.FEED_SIZE
        )