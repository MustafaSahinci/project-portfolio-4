from . import views
from django.urls import path

urlpatterns = [
    path("blog/", views.PostList.as_view(), name="blog"),
    path("", views.Home.as_view(), name="home"),
    path("post_create/", views.CreatePost.as_view(), name="post_create"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
