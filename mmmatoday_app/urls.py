from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('loginpage', views.loginpage),
    path('register', views.register),
    path('regpage', views.regpage),
    path('logout', views.logout),
    path('news', views.news),
    path('gyms', views.gyms),
    path('training', views.training),
    path('createpost', views.createpost),
    path('deletepost/<int:id>', views.deletepost),
    path('postcomment/<int:post_id>', views.postcomment),
    path('deletecomment/<int:id>', views.deletecomment),
    path('inbox', views.inbox),
    path('viewmessage/<int:id>', views.viewmessage),
    path('createmessage/<int:receiverid>', views.createmessage),
    path('deletemessage/<int:msg_id>', views.deletemessage),
    path('viewuser/<int:id>', views.viewuser),
    path('edituser', views.edituser),
    path('updateuser/<int:id>', views.updateuser),
]