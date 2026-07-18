from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import CommentSerializer
from ..services.lifeCycle import CommentLifeCycle
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@login_required
@api_view(["POST"])
def commentPost(request, postId):

    serializer = CommentSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    comment = CommentLifeCycle.comment_post(
        request.user,
        postId,
        serializer.validated_data,
        request.data.get("reply_of")
    )

    return Response(
        CommentSerializer(comment).data,
        status=status.HTTP_201_CREATED
    )

@csrf_exempt
@login_required
@api_view(["DELETE"])
def deleteComment(request, commentId):

    comment = CommentLifeCycle.delete_comment(
        request.user,
        commentId
    )

    if comment is None:
        return Response(
            {"detail": "You cannot delete this comment."},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )