from django.urls import path
from auth.views import LoginView, RegisterView, LogoutView, LogoutAllView

app_name = 'auth'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='knox_register'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', LogoutAllView.as_view(), name='knox_logoutall'),
]
