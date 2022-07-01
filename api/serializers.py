from rest_framework import serializers
from . import models

class customerDataSerializer(serializers.ModelSerializer):
    initialDeposit = serializers.IntegerField(min_value=500, max_value=1000000)
    accountName = serializers.CharField(max_length=50, min_length=5)
    class Meta:
        model = models.customer
        fields = ["accountName","password","initialDeposit"]
        

class depositDataSerializer(serializers.ModelSerializer):
    accountNumber = serializers.CharField(max_length=10, min_length=10)
    class Meta:
        model = models.transaction
        fields = ["amount","accountNumber"]

class loginDataSerializer(serializers.ModelSerializer):
    accountNumber = serializers.CharField(max_length=10, min_length=10)
    class Meta:
        model = models.customer
        fields = ["accountNumber","password"]
class transactionSerializer(serializers.ModelSerializer):
    accountNumber = serializers.CharField(max_length=10, min_length=10)
    class Meta:
        model = models.customer
        fields = ["accountNumber"]
