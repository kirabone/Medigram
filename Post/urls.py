from django.urls import path
from .views import lifeCycle, interactions, show

urlpatterns = [

    path("createpost/", lifeCycle.create),
    path("deletepost/", lifeCycle.delete_post),
    path("updatepost/", lifeCycle.update_post),
    path("likepost/<int:postid>", interactions.like_post),
    path("savepost/<int:postid>/", interactions.save_post),
    path("savedpost/", show.saved_posts),
    path("feed/home/", show.feed, {"types": "home"}),
    path("feed/reels/", show.feed, {"types": "reels"}),
    path("feed/posts/", show.feed, {"types": "posts"}),
    path("feed/texts/", show.feed, {"types": "texts"}),


]