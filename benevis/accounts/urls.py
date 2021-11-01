from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("<str:username>/", views.UserDahboard.as_view(), name="dashboard"),
    path("follow/user/", views.Follow.as_view(), name="follow"),
    path("unfollow/user/", views.Unfollow.as_view(), name="unfollow"),
    path("search/user/", views.SearchQuery.as_view(), name="searchQuery"),
]