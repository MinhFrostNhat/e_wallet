
from email.policy import default
from this import s
from uuid import uuid4
from django.forms import CharField
from rest_framework import serializers, status
from .models import Account, Merchant,Transaction

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('id','balance')

class MerchatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'
        read_only_fields = ('merchant_id','api_key','account_id')





class Nested(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('transactionId','income_account_id','outcome_account_id','status')






