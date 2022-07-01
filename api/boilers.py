import hashlib
from random import randint

from .models import customer

def hashpassword(password :str) -> str :
    encoded = password.encode("utf-8")#encode the password
    hashed = hashlib.sha256(encoded).hexdigest() 
    return hashed

def generateAccountNumber() -> int:
    """
    Generates random 10 digits  Account number 
    """
    n = 10
    range_start = 10**(n-1)
    range_end = (10**n)-1
    accountNumber = randint(range_start, range_end)
    return accountNumber

def gen_accountNumberUnique(accountNumber: int) -> int:
    """
    Checks for uniqueness of account number and 
    """
    
    unique = False
    while not unique:
        accountNumberqs = customer.objects.filter(accountNumber=accountNumber)
        if not accountNumberqs.exists():
            unique = True
            return accountNumber
        else:
            accountNumber = generateAccountNumber()

def accountNameUnique(accountName) -> bool:
    """
    checks for uniqueness of accountName
    """
    accountNameqs = customer.objects.filter(accountName = accountName)
    if accountNameqs.exists():
        unique = False
        return unique
    else:
        unique = True
        return unique
