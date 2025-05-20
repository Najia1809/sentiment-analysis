from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),

    # Main Sentiment App View
    path('home/', views.home, name="home"),
]







