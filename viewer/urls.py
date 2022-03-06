from django.urls import path
from .views import gif_page, login_user, register_user, log_out

urlpatterns = [

    path('', login_user, name='login'),
    path('logout/', log_out, name='logout'),
    path('gif/', gif_page, name='home'),
    path('register/', register_user, name='register'),

    ]