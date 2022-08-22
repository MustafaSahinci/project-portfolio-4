from . import views
from django.urls import path

urlpatterns = [
    path("post_create/", views.post_create, name="post_create"),
    path("edit/<slug:slug>", views.post_edit, name="post_edit"),
    path("delete/<slug:slug>", views.post_delete, name="post_delete"),
    path("category/<str:cats>", views.categories, name="categories"),
    path("blog/", views.PostList.as_view(), name="blog"),
    path("", views.Home.as_view(), name="home"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
