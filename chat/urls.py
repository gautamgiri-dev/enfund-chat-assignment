from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("chat", views.chat, name="chat"),
    path("api/v1/get-messages", views.get_messages, name="get_messages"),
    path("api/v1/send-message", views.send_message, name="send_message"),
]