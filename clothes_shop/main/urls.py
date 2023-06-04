

from . import views
from django.urls import path


urlpatterns = [
    path('', views.page),
    path('registr/', views.regist),
    path('check/', views.check, name='check'),
    path('advertisement/', views.advertisement),
    path('posts/', views.posts),
    path('payment/', views.payment_view),
    path('successful/', views.payment_successful)



]
