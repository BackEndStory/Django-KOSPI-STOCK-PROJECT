from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'common'

urlpatterns=[

  path('', auth_views.LoginView.as_view(template_name='search/secondmain.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='search/firstmain.html'), name='logout'),
  path('new_account/', views.register, name='register'),
  path('forgot_id/', views.ForgotIDview, name='ForgotIDview'),
  path('login/forgot_pw/', views.ForgotPWview, name='ForgotPWview'),




]