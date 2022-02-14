# Generated by Django 4.0.2 on 2022-02-14 18:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('account_type', models.CharField(choices=[('personal', 'personal'), ('merchant', 'merchant'), ('issuer', 'issuer')], default='personal', max_length=20)),
                ('balance', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('merchant_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('merchantName', models.CharField(max_length=200)),
                ('merchantUrl', models.CharField(default='http://localhost:8080', max_length=200)),
                ('api_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transactionId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('extraData', models.CharField(max_length=255)),
                ('signature', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('CREATE', 'CREATE'), ('CONFIRM', 'CONFIRM'), ('VERIFY', 'VERIFY'), ('CANCEL', 'CANCEL'), ('EXPIRE', 'EXPIRE'), ('SUCCESS', 'SUCCESS')], default='CREATE', max_length=20)),
                ('income_account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='income', to='run_wallet.account')),
                ('merchant_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='run_wallet.merchant')),
                ('outcome_account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outcome', to='run_wallet.account')),
            ],
        ),
    ]
