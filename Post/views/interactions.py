from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Profile.models import Follow, FollowRequest, Block, Profile
from ..models import Post
from ..serializers import PostSerializer
from ..services.interactions import PostInteractions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def like_post(request, postid):

    if request.method == "POST":

        PostInteractions.like_post(
            request.user,
            postid
        )

        return Response(
            status=status.HTTP_201_CREATED
        )

    PostInteractions.unlike_post(
        request.user,
        postid
    )

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )

@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def save_post(request, postid):

    if request.method == "POST":

        PostInteractions.save_post(
            request.user,
            postid
        )

        return Response(
            status=status.HTTP_201_CREATED
        )

    PostInteractions.unsave_post(
        request.user,
        postid
    )

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )








