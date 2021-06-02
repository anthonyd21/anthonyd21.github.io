from django.urls import path

from . import views

urlpatterns = [
    path("posting/",views.index,name="index"),
    path("posting/posts",views.posts,name="posts")
]