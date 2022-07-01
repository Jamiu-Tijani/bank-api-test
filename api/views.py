from datetime import datetime
from urllib import response
from flask import has_app_context

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .boilers import accountNameUnique, gen_accountNumberUnique, generateAccountNumber, hashpassword
from .models import customer, transaction

from .serializers import customerDataSerializer, depositDataSerializer, loginDataSerializer, transactionSerializer

class account_creation(generics.GenericAPIView):
    serializer_class = customerDataSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
            customer_data =request.data
            accountName = customer_data['accountName']
            password = customer_data['password']
            initialDeposit = int(customer_data["initialDeposit"])
            acc_num = generateAccountNumber()
            accountNumber =  gen_accountNumberUnique(accountNumber = acc_num)
            if accountNameUnique(accountName=accountName) and initialDeposit >= 500 :
                customer_ = customer.objects.create(accountName=accountName,accountNumber=accountNumber,password = hashpassword(password),accountBalance=initialDeposit)
                customer_.save
                transaction.objects.create(customer=customer_,amount=initialDeposit,transactionType = "Deposit" ,accountBalance = customer_.accountBalance,narration="Initial Deposit")
                transaction.save

                context = {
                    "responseCode": 200,
                    "success": True,
                    "Descr": "Account {} Created SuccessFully".format(acc_num),}
                return Response(context,status=status.HTTP_201_CREATED) 
            elif initialDeposit < 500:
                context = {
                    "responseCode": 51,
                    "success": False,
                    "Descr": "Initial deposit must be greater or equal to 500",
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

            elif not accountNameUnique(accountName=accountName):
                context = {
                    "responseCode": 409,
                    "success": False,
                    "Descr": "User Already exists",}
                return Response(context,status=status.HTTP_409_CONFLICT) 

class deposit(generics.GenericAPIView):
    serializer_class = depositDataSerializer
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        data = request.data
        accountNumber = data["accountNumber"]
        amount = float(data["amount"])
        accountNumberqs = customer.objects.filter(accountNumber=accountNumber)
        if accountNumberqs.exists():
            
            customer_ = customer.objects.get(accountNumber=accountNumber) 
            if amount<100 or amount > 1000000:
                context = {
                    "responseCode": 404,
                    "success": False,
                    "message": "deposit amount must not be less than 100 or greater than 1000000"

                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            new_bal = amount + customer_.accountBalance
            customer_.accountBalance = new_bal
            customer_.save()
            transaction.objects.create(customer = customer_,amount=amount,narration="deposited {} on {}".format(amount,datetime.now()),accountBalance=customer_.accountBalance,transactionType = "Deposit")
            transaction.save
            context = {
                    "responseCode": 201,
                    "success": True,
                    "message": "{} deposited successfully to account {} on {}".format(amount,accountNumber,datetime.now()),}
            return Response(context,status=status.HTTP_201_CREATED)
        else:
            context = {
                    "responseCode": 404,
                    "success": False,
                    "message": "{} does not exist".format(accountNumber)}
            return Response(context,status=status.HTTP_404_NOT_FOUND)

class withdraw(generics.GenericAPIView):
    serializer_class = depositDataSerializer
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        data = request.data
        accountNumber = data["accountNumber"]
        amount = float(data["amount"])
        accountNumberqs = customer.objects.filter(accountNumber=accountNumber)
        if accountNumberqs.exists():
            customer_ = customer.objects.get(accountNumber=accountNumber)
            if amount >= customer_.accountBalance or amount < 100:
                new_bal = customer_.accountBalance - amount
                if new_bal <= 500:
                    context = {
                        "responseCode": 51,
                        "success": False,
                        "message": "Insufficient Funds remaining account balance after withdrawal must be greater than 500"

                    }
                    return Response(context, status.HTTP_400_BAD_REQUEST)

                customer_.accountBalance = new_bal
                customer_.save()
                transaction.objects.create(customer = customer_,amount=amount,narration="withdrawn {} on {}".format(amount,datetime.now()),accountBalance=customer_.accountBalance,transactionType = "Withdrawal")
                transaction.save
                context = {
                        "responseCode": 201,
                        "success": True,
                        "message": "{} withdrawn successfully from account {} on {}".format(amount,accountNumber,datetime.now()),}
                return Response(context,status=status.HTTP_201_CREATED)
            else:
                context = {
                        "responseCode": 400,
                        "success": False,
                        "message": "Insufficient Funds",}
                return Response(context,status=status.HTTP_400_BAD_REQUEST)

        else:
            context = {
                    "responseCode": 404,
                    "success": False,
                    "message": "{} does not exist".format(accountNumber)}
            return Response(context,status=status.HTTP_404_NOT_FOUND)




class account_info(generics.GenericAPIView):
    serializer_class = loginDataSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = request.data
        accountNumber = data["accountNumber"]
        password = data["password"]
        accountNumberqs = customer.objects.filter(accountNumber=accountNumber)
        if accountNumberqs.exists:
            customer_ = customer.objects.get(accountNumber=accountNumber) 
            if hashpassword(password) == customer_.password:
                context = {
                    "responseCode":200,
                    "success": True,
                    "message": "",
                    "account":{
                        "accountName":customer_.accountName,
                        "accountNumber": customer_.accountNumber,
                        "accountBalance": customer_.accountBalance,

                    }

                }
                return Response(context, status.HTTP_200_OK)
            else:
                context = {
                    "responseCode":401,
                    "success": False,
                    "message": "",


                }
                return Response(context, status.HTTP_401_UNAUTHORIZED)
        else:
            context = {
                "responseCode":401,
                "success": False,
                "message": "",

            }
            return Response(context, status.HTTP_401_UNAUTHORIZED)


class login(generics.GenericAPIView):
    serializer_class = loginDataSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = request.data
        accountNumber = data["accountNumber"]
        password = data["password"]
        accountNumberqs = customer.objects.filter(accountNumber=accountNumber)
        if accountNumberqs.exists:
            customer_ = customer.objects.get(accountNumber=accountNumber) 
            if hashpassword(password) == customer_.password:
                context = {
                    "responseCode":200,
                    "success": True,
                    "message": "Login Successfull",
        

                }
                return Response(context, status.HTTP_200_OK)
            else:
                context = {
                    "responseCode":401,
                    "success": False,
                    "message": "Login Failed",


                }
                return Response(context, status.HTTP_401_UNAUTHORIZED)
        else:
            context = {
                "responseCode":401,
                "success": False,
                "message": "Login Failed",

            }
            return Response(context, status.HTTP_401_UNAUTHORIZED)


class transactionHistory(generics.GenericAPIView):
    serializer_class = transactionSerializer
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        data = request.data
        accountNumber = data["accountNumber"]
        accountNumberqs = customer.objects.filter(accountNumber=accountNumber)
        if accountNumberqs.exists():
            customer_ = customer.objects.get(accountNumber=accountNumber)
            transaction_history = transaction.objects.filter(customer=customer_)
            transactions = []
            for transaction_ in transaction_history:
                obj = {}
                obj["Date"] = transaction_.transactionDate,
                obj["transactionType"] =  transaction_.transactionType,
                obj["Narration"] = transaction_.narration
                obj["Amount"] = transaction_.amount
                obj["accountBalance"] = transaction_.accountBalance
                transactions.append(obj)


            context = {
            "account_statement": transactions,
            }
            return Response(context, status = status.HTTP_200_OK)
        else:
            context = {
                "responseCode":404,
                "success": False,
                "message": "account {} does not exist in our records".format(accountNumber),

            }
            return Response(context, status.HTTP_404_NOT_FOUND)




