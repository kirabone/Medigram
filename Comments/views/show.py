from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers import CommentSerializer
from ..services.show import CommentShow


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def comments(request, post_id):

    offset = int(request.GET.get("offset", 0))

    comments = CommentShow.comments(
        request.user,
        post_id,
        offset
    )

    return Response(
        CommentSerializer(
            comments,
            many=True
        ).data
    )