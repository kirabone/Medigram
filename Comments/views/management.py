from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..services.management import CommentManagement


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def pin_comment(request, comment_id):

    if request.method == "POST":

        CommentManagement.pin(
            request.user,
            comment_id
        )

        return Response({
            "message": "Comment pinned."
        })

    CommentManagement.unpin(
        request.user,
        comment_id
    )

    return Response({
        "message": "Comment unpinned."
    })

@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def heart_comment(request, comment_id):

    if request.method == "POST":

        CommentManagement.heart(
            request.user,
            comment_id
        )

        return Response({
            "message": "Comment hearted."
        })

    CommentManagement.unheart(
        request.user,
        comment_id
    )

    return Response({
        "message": "Comment unhearted."
    })

    CommentManagement.unheart(
        request.user,
        comment_id
    )

    return Response({
        "message": "Comment unhearted."
    })