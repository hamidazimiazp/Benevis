from django.urls import path
from . import views

app_name = "twitte"
urlpatterns = [
    path("new_twitte/<int:user_id>/", views.CreateTwitte.as_view(), name="createTwitte"),
    path("delete_twitte/<int:user_id>/<int:twt_id>", views.DeleteTwitte.as_view(), name="deleteTwitte"),
    path("like/<int:twitte_id>/", views.MakeVote.as_view(), name="makeVote"),
    path("unlike/<int:twitte_id>/", views.DeleteVote.as_view(), name="deleteVote"),
    path("twitte/<int:id>/<int:year>/<int:month>/<int:day>/", views.TwitteDetail.as_view(), name="twitteDetail"),
    path("twitte/<int:twitte_id>/comment/", views.CreateComment.as_view(), name="createComment"),
    path("friends/twitte/", views.FriendsTwittes.as_view(), name="friendsTwittes"),
]