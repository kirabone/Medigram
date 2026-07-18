from django.urls import path
from .views import interaction , lifeCycle , management , show

urlpatterns = [
    path("createcomment/<int:post_id>/", lifeCycle.commentPost),
    path("deletecomment/<int:comment_id>/", lifeCycle.deleteComment),
    path("likecomment/<int:comment_id>/", interaction.like_comment),
    path("pincomment/<int:comment_id>/", management.pin_comment),
    path("heartcomment/<int:comment_id>/", management.heart_comment),
    path("comment/<int:post_id>/",show.comments)
]