from django.urls import path

from . import views

urlpatterns = [
    path('accounts/signup', views.SignUpView.as_view(), name='signup_view'),
    path('accounts/signup/register/', views.signup, name='signup'),

    path('accounts/login/', views.LoginView.as_view(), name='login_view'),
    path('accounts/login/register/', views.login_user, name='login_user'),

    path('accounts/customize_user/', views.CustomizeUserView.as_view(), name='customize_user_view'),
    path('accounts/customize_user/register/', views.customize_user, name='customize_user'),
]


