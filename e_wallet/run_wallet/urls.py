from django import views
from django.urls import path,re_path
from .views import Sign_Up_Views,Merchart_Sign_Up_Views,account_token,Topup,Transac_Views
from rest_framework_simplejwt import views as jwt_views
  
app_name = 'run_wallet'

urlpatterns = [
    path('account/signup/',Sign_Up_Views.as_view(), name='index'),
    path('merchart/signup/',Merchart_Sign_Up_Views.as_view(), name='index1'),
    path('<accid>/token',
         account_token.as_view(), name='acc'),
    path('<accid>/topup',
         Topup.as_view(), name='acc1'),
         path('transation/create',
         Transac_Views.as_view(), name='acc2'),
     path('api/token/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),

]