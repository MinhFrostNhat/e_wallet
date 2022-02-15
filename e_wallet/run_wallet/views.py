

from django.conf import settings

from rest_framework import generics, permissions, serializers, viewsets, status

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Account,Merchant,Transaction
from .serializers import AccountSerializer,MerchatSerializer,generate_access_token,generate_refresh_token,Nested

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import exceptions
import re
import jwt,datetime

class Sign_Up_Views(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class Merchart_Sign_Up_Views(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchatSerializer
  

class Transac_Views(APIView):
    serializer_class = Nested
    def post(self, request):
            token = request.COOKIES.get('accesstoken')

            if not token:
                raise AuthenticationFailed('Unauthenticated!')

            try:
                 payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')

            if payload['account_type'] == "merchant":
                serializer = Nested(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else: 
                return Response('not ok',status.HTTP_401_UNAUTHORIZED)

    
class account_token(generics.RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = (permissions.AllowAny,)
    queryset=Account.objects.all()
    def get(self, request, format=None,**kwargs):
        user = Account.objects.get(account_id=kwargs["accid"])
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')

        serialized_user = AccountSerializer(user).data

        access_token = generate_access_token(user)
        response = Response()
        response.set_cookie(key ='accesstoken',value=access_token,httponly=True)
        response.data = {
            'accesstoken': str(access_token)
        }
        return response
        
    


class Topup(APIView):
    queryset = Account.objects.all()
    def post(self, request, format=None,**kwargs):
        token = request.COOKIES.get('accesstoken')

        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                 payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                 if payload['account_type'] == "issuer":
                     user = Account.objects.filter(account_id=kwargs["accid"]).first()
                     if user.account_type == "issuer":
                        account_id = request.data['account_id']
                        amount = request.data['amount']
                        check = Account.objects.filter(account_id = account_id).first()
                        if check.account_type == "personal":
                            a = float(amount)
                            account_balance =Account.objects.filter(account_id = account_id).first()
                            if not account_balance:
                                return
                            c= account_balance.balance
                            b = float(c)
                            x = Account.objects.filter(account_id = account_id).update(balance = b+ a)
                            return Response(status = status.HTTP_200_OK)
                        else: return Response("not ok",status=status.HTTP_400_BAD_REQUEST)
                     else: return Response("not ok",status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')

    
class Comfirm:
    pass

class verify:
    pass

class Cancel:
    pass


"""

class Merchart_Sign_Up_Views(generics.CreateAPIView):
        queryset = Merchant.objects.all()
        serializer_class = MerchatSerializer
        def get(self, request):
            token = request.COOKIES.get('accesstoken')

            if not token:
                raise AuthenticationFailed('Unauthenticated!')

            try:
                 payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')

            return Response('ok')
"""