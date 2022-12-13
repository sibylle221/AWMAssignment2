from django.urls import path #re_path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),

    path('', world, name='world'),
    path('update_location/', update_location, name="update_location"),
    # path('', include('pwa.urls')),
    # re_path('login/', user_login, name='login'),
    # re_path('logout/', user_logout, name='logout'),
    # re_path('register/', user_register, name='register'),
]