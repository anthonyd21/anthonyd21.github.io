from django.urls import path

from . import views

urlpatterns = [
    path("ui/", views.index, name="index"),
    path("ui/sections/<int:num>",views.section,name="section")
]