from django.urls import include,path
from django.conf.urls import url
from . import views

app_name='user'


urlpatterns = [
    path('',views.index,name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('newpost/', views.newpost, name='newpost'),
    path('<str:name>/',views.userpage,name='userpage')
]
