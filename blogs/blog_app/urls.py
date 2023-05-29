# blog_app/urls.py

from django.urls import path

from .views import (  # noqa: E501
    BlogDetailView,
    BlogListView,
    CommentCreateView,
    CommentReplyView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
)

urlpatterns = [
    path("blogs/", BlogListView.as_view(), name="blog-list"),
    path("comments/", CommentCreateView.as_view(), name="comment-create"),
    path(
        "comments/<int:comment_id>/reply/",
        CommentReplyView.as_view(),
        name="comment-reply",
    ),  # noqa: E501
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path("blogs/", BlogListView.as_view(), name="blog-list"),
    path("blogs/<int:blog_id>/", BlogDetailView.as_view(), name="blog-detail"),
]
