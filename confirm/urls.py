from django.urls import path
from . import views

app_name='confirm'

urlpatterns = [
    path('', views.home , name='home'),
    path('register/',views.registration_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('logedin/', views.logedin,name='logedin'),
]
