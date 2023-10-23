from django.urls import path, re_path, reverse
from pages import views

urlpatterns = [
    path("", views.home, name='home'),
    path('login/', views.login, name='login'),
    path('trainee/signup/', views.signup, name='signup'),
    path('api/v1/infobip/content/', views.InfobipContent.as_view()),
]
