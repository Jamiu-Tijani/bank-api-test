from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
# Create your models here.

class customer(models.Model):
    accountName = models.CharField(max_length=500)
    password = models.CharField(max_length=5000)
    accountBalance = models.FloatField(default=0)
    accountNumber = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.accountName

class transaction(models.Model):
    transaction_types = (("WD","Withdrawal"),("DS","Deposit"))
    transactionType = models.CharField(default=None,max_length=300,choices=transaction_types)
    customer = models.ForeignKey(customer, on_delete=models.SET_NULL, blank = True, null = True)
    transactionDate = models.DateField(auto_now_add=True)
    amount = models.FloatField()
    accountBalance = models.FloatField()
    narration = models.CharField(max_length=5000, default=None)
    def __str__(self) -> str:
        return self.transactionType

