# Generated by Django 5.1.6 on 2025-02-23 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
        ('users', '0002_account_loancustomer_loanprovider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans_taken', to='users.loancustomer'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='users.loanprovider'),
        ),
    ]
