from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer,CommentSerializer, SaveSerializer, FeedRequestSerializer
from .services import PostService
from .serializers import PostSerializer
from .services import FeedService

@csrf_exempt
@login_required
@api_view(["POST"])
def createPost(request):

    serializer = PostSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    post = PostService.create_post(
        request.user,
        serializer.validated_data
    )

    return Response(
        PostSerializer(post).data,
        status=status.HTTP_201_CREATED
    )


@csrf_exempt
@login_required
@api_view(["GET"])
def getPost(request, postId):

    post = PostService.get_post(postId)

    serializer = PostSerializer(post)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )

@csrf_exempt
@login_required
@api_view(["DELETE"])
def deletePost(request, postId):

    post = PostService.delete_post(
        request.user,
        postId
    )

    if post is None:
        return Response(
            {"detail": "You cannot delete this post."},
            status=status.HTTP_403_FORBIDDEN
        )

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )


@csrf_exempt
@login_required
@api_view(["POST"])
def likePost(request, postId):

    like = PostService.like_post(
        request.user,
        postId
    )

    return Response(
        status=status.HTTP_201_CREATED
    )


@csrf_exempt
@login_required
@api_view(["DELETE"])
def unlikePost(request, postId):

    PostService.unlike_post(
        request.user,
        postId
    )

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )


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

    comment = PostService.comment_post(
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

    comment = PostService.delete_comment(
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


@csrf_exempt
@login_required
@api_view(["POST"])
def savePost(request, postId):

    save = PostService.save_post(
        request.user,
        postId
    )

    return Response(
        SaveSerializer(save).data,
        status=status.HTTP_201_CREATED
    )


@csrf_exempt
@login_required
@api_view(["DELETE"])
def unsavePost(request, postId):

    PostService.unsave_post(
        request.user,
        postId
    )

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(["GET"])
def feed(request):

    serializer = FeedRequestSerializer(
        data={
            "types": request.GET.getlist("type")
        }
    )

    serializer.is_valid(raise_exception=True)

    posts = FeedService.get_feed(
        user=request.user,
        **serializer.validated_data,
    )

    return Response(
        PostSerializer(posts, many=True).data
    )

@csrf_exempt
@login_required
@api_view(["GET"])
def profilePosts(request, userId):

    posts = PostService.profile_posts(userId)

    serializer = PostSerializer(
        posts,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@csrf_exempt
@login_required
@api_view(["GET"])
def profileReels(request, userId):

    reels = PostService.profile_reels(userId)

    serializer = PostSerializer(
        reels,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@csrf_exempt
@login_required
@api_view(["GET"])
def profileTexts(request, userId):

    texts = PostService.profile_texts(userId)

    serializer = PostSerializer(
        texts,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@csrf_exempt
@login_required
@api_view(["GET"])
def savedPosts(request):

    posts = PostService.saved_posts(request.user)

    serializer = PostSerializer(
        posts,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


def uploadPostForm(request):
    return render(request, 'Post/uploadPost.html')



    