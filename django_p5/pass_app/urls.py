from django.urls import path
from pass_app import views

app_name='pass_app'

urlpatterns = [
    
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('',views.index,name='index')
]