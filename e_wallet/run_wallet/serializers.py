from rest_framework.response import Response
from rest_framework import serializers, status
from .models import Account, Merchant,Transaction

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('account_id','balance')

class MerchatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'
        read_only_fields = ('merchant_id','api_key','account_id')


import datetime
import jwt
from django.conf import settings


def generate_access_token(user):

    payload = {
        'account_id': str(user.account_id),
        'account_type': user.account_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=15),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token

def merchant_tokenize(merchant_id, signature, api_key):
    try:
        token = jwt.encode({
            'merchant_id': merchant_id,
            'signature': signature,
            'exp': datetime.utcnow() + datetime.timedelta(minutes=300)
        }, api_key, algorithm='HS256')
        return {'data': token}
    except Exception as err:
    
        return Response("error")

def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': str(user.account_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])

    return refresh_token


class Nested(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('transactionId','status')
