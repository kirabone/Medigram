from django.contrib.auth.models import User
from .models import (
    Comment,
)
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"