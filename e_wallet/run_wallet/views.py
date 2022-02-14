from re import U
from rest_framework import generics, permissions, serializers, viewsets, status

from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import Account,Merchant,Transaction
from .serializers import AccountSerializer,MerchatSerializer, Nested

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
import jwt,datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class Sign_Up_Views(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class Merchart_Sign_Up_Views(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchatSerializer
    permission_classes = (IsAuthenticated,)



class Transac_iews(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = Nested

    
    
class account_token(generics.RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = (permissions.AllowAny,)
    queryset=Account.objects.all()
    def get(self, request, format=None,**kwargs):
        user = Account.objects.get(account_id=kwargs["accid"])
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')

        serialized_user = AccountSerializer(user).data

        access_token = AccessToken.for_user(user)

        return Response(str(access_token))
        


class Topup(APIView):

    queryset = Account.objects.all()
    def post(self, request, format=None,**kwargs):
        user = Account.objects.get(account_id=kwargs["id"])
        account_id = request.data['account_id']
        amount = request.data['amount']
        check = Account.objects.filter(account_id = account_id)
        if check:
            a = float(amount)
            account_balance =Account.objects.filter(account_id = account_id).first()
            if not account_balance:
                return
            c= account_balance.balance
            b = float(c)
            x = Account.objects.filter(account_id = account_id).update(balance = b+ a)
            return Response(status = status.HTTP_200_OK)
        return user
