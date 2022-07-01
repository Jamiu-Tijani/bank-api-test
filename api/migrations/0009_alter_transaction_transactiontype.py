# Generated by Django 3.2.11 on 2022-07-01 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_transaction_transactiontype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transactionType',
            field=models.CharField(choices=[('WD', 'Withdrawal'), ('DS', 'Deposit')], default=None, max_length=300),
        ),
    ]