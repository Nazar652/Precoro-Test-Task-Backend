from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('check/', check_authentication, name='check')
]