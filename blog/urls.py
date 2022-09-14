from . import views
from django.urls import path

"""url for the views and templates"""
urlpatterns = [
    path("post_create/", views.PostCreate.as_view(), name="post_create"),
    path("edit/<slug:slug>", views.PostEdit.as_view(), name="post_edit"),
    path("delete/<slug:slug>", views.PostDelete.as_view(), name="post_delete"),
    path("category/<str:cats>", views.categories, name="categories"),
    path("<int:pk>/profile", views.ProfileDetails.as_view(),
         name="profile_detail"),
    path("<int:pk>/profile_edit", views.ProfileEdit.as_view(),
         name="profile_edit"),
    path("profile_create", views.ProfileCreate.as_view(),
         name="profile_create"),
    path("blog/", views.PostList.as_view(), name="blog"),
    path("", views.Home.as_view(), name="home"),
    path("post/<slug:slug>", views.PostDetail.as_view(), name="post_detail"),
    path("like/<slug:slug>", views.PostLike.as_view(), name="post_like"),
    path("<int:pk>/comment_delete", views.CommentDelete.as_view(),
         name="comment_delete"),
    path("<int:pk>/comment_edit", views.CommentEdit.as_view(),
         name="comment_edit"),
]
