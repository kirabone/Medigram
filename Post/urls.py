from django.urls import path
from . import views

urlpatterns = [

    # UI
    path("upload/", views.uploadPostForm, name="uploadPostForm"),

    # CRUD
    path("create/", views.createPost, name="createPost"),
    path("<int:postId>/", views.getPost, name="getPost"),
    #path("<int:postId>/update/", views.updatePost, name="updatePost"),
    path("<int:postId>/delete/", views.deletePost, name="deletePost"),

    # Feed
    path("feed/", views.feed, name="feedPosts"),

    # Profile
    path("profile/<int:userId>/posts/", views.profilePosts, name="profilePosts"),
    path("profile/<int:userId>/reels/", views.profileReels, name="profileReels"),
    path("profile/<int:userId>/texts/", views.profileTexts, name="profileTexts"),

    # Saved
    path("saved/", views.savedPosts, name="savedPosts"),

    # Likes
    path("<int:postId>/like/", views.likePost, name="likePost"),
    path("<int:postId>/unlike/", views.unlikePost, name="unlikePost"),

    # Comments
    path("<int:postId>/comment/", views.commentPost, name="commentPost"),
    #path("comment/<int:commentId>/update/", views.updateComment, name="updateComment"),
    path("comment/<int:commentId>/delete/", views.deleteComment, name="deleteComment"),

    # Saves
    path("<int:postId>/save/", views.savePost, name="savePost"),
    path("<int:postId>/unsave/", views.unsavePost, name="unsavePost"),

    # Misc
    #path("<int:postId>/share/", views.sharePost, name="sharePost"),
    #path("<int:postId>/report/", views.reportPost, name="reportPost"),
    #path("<int:postId>/hide/", views.hidePost, name="hidePost"),
]