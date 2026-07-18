from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import PostSerializer
from ..services.lifeCycle import PostLifeCycle
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@login_required
@api_view(["POST"])
def create(request):
    serializer = PostSerializer(data=request.data)  #data validation

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    post = PostLifeCycle.create_post(
        user=request.user,
        validated_data=serializer.validated_data
    )   #using function

    return Response(
        PostSerializer(post).data,
        status=201
    )

@csrf_exempt
@login_required
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):

    PostLifeCycle.delete_post(
        user=request.user,
        post_id=post_id
    )

    return Response(
        {"message": "Post deleted successfully."},
        status=status.HTTP_200_OK
    )

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_post(request, post_id):

    caption = request.data.get("caption")

    post = PostLifeCycle.update_post(
        user=request.user,
        post_id=post_id,
        caption=caption
    )

    return Response(
        PostSerializer(post).data,
        status=status.HTTP_200_OK
    )


