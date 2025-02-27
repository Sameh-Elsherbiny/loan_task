# Generated by Django 5.1.6 on 2025-02-24 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_alter_loan_loan_customer_alter_loan_loan_provider'),
        ('users', '0002_account_loancustomer_loanprovider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_status',
            field=models.CharField(choices=[('RQ', 'Requested'), ('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected'), ('PD', 'Paid')], default='P', max_length=10),
        ),
        migrations.CreateModel(
            name='LoanRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='loan.loan')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_requests', to='users.loanprovider')),
            ],
        ),
    ]
