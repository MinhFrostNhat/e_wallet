from email.policy import default
import uuid
from django.db import models
from django.shortcuts import reverse
import hashlib

class Account(models.Model):
    PERSONAL = 'personal'
    MERCHANT = 'merchant'
    ISSUER = 'issuer'
    STATUSES = (
        (PERSONAL, PERSONAL),
        (MERCHANT, MERCHANT),
        (ISSUER, ISSUER),
    )
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,verbose_name='id')
    account_type = models.CharField(
        max_length=20, choices=STATUSES, default=PERSONAL)
    balance = models.FloatField(default=0)

    def __str__(self):
        return f'{self.account_id},{self.balance}'

    def get_absoluted_url(self):
        return self.balance

class Merchant(models.Model):
    merchant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchantName = models.CharField(max_length=200,blank=False)
    merchantUrl = models.CharField(max_length=200,default='http://localhost:8080')
    api_key = models.UUIDField(default=uuid.uuid4, editable=False)
    account_id = models.UUIDField(default=uuid.uuid4, editable=False)

class Transaction(models.Model):
    FAILED= 'FAILED'
    INITIALIZED= 'INITIALIZED'
    CONFIRM = 'CONFIRM'
    VERIFY = 'VERIFY'
    CANCEL ='CANCEL'
    EXPIRE = 'EXPIRE'
    COMPLETED = 'COMPLETED'
    STATUSES = (
        (FAILED,FAILED),
        (INITIALIZED, INITIALIZED),
        (CONFIRM, CONFIRM),
        (VERIFY, VERIFY),
        (CANCEL,CANCEL),
        (EXPIRE,EXPIRE),
        (COMPLETED,COMPLETED),
    )
    transactionId =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    extraData = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUSES, default=INITIALIZED,editable=False)
    merchant_id = models.ForeignKey(Merchant,on_delete=models.CASCADE, null=True)
    income_account_id = models.ForeignKey(Account,on_delete=models.CASCADE, null=True,related_name='income')
    outcome_account_id = models.ForeignKey(Account,on_delete=models.CASCADE, null=True,related_name='outcome')
    signature = models.CharField(default=hashlib.md5((str(merchant_id)+str(amount)+str(extraData)).encode()).hexdigest()
                             , max_length=255)
    
    def confirm_update(self):
        self.status = 'CONFIRM'
        self.save()
    
    def verify_update(self):
        self.status = 'VERIFY'
        self.save()

    def cancel_update(self):
        self.status = 'CANCEL'
        self.save()

    def fail_update(self):
        self.status = 'FAILED'
        self.save()
    
    def completed_update(self):
        self.status = 'COMPLETED'
        self.save()


