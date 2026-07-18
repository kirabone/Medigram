from django.contrib.auth.models import User
from .models import (
    Post,
    Like,
    Save,
    Share,
)
from rest_framework import serializers
from .models import Post

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]

class PostSerializer(serializers.ModelSerializer):

    uploader = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = "__all__"



class SaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Save
        fields = "__all__"

class ShareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Share
        fields = "__all__"

class FeedRequestSerializer(serializers.Serializer):

    types = serializers.ListField(
        child=serializers.ChoiceField(
            choices=Post.PostType.choices
        )
    )