from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..services.interactions import CommentInteractions



@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):

    if request.method == "POST":

        CommentInteractions.like(
            request.user,
            comment_id
        )

        return Response({
            "message": "Comment liked."
        })

    CommentInteractions.unlike(
        request.user,
        comment_id
    )

    return Response({
        "message": "Comment unliked."
    })

    CommentInteractions.unlike(
        request.user,
        comment_id
    )

    return Response({
        "message": "Comment unliked."
    })