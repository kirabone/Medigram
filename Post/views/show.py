from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Profile.models import Follow, FollowRequest, Block, Profile
from ..models import Post
from ..serializers import PostSerializer
from ..services.show import PostShow
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

@csrf_exempt
@login_required
@api_view(["GET"])
def saved_posts(request):

    posts = PostShow.saved_posts(request.user)

    serializer = PostSerializer(
        posts,
        many=True
    )

    return Response(
        serializer.data,
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request, types):

    types = [
        t.strip().upper()
        for t in types.split(",")
    ]

    posts = PostShow.generate_feed(
        request.user,
        types
    )

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)