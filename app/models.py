from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class LoanRequests(models.Model):
    loanNumber = models.AutoField(primary_key=True)
    userID = models.IntegerField(default=0)
    dateCreated = models.DateField(default=timezone.now)
    dateApproved = models.DateField(null=True, blank=True)
    dateSubmitted = models.DateField(null=True, blank=True)
    dateDenied = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.loanNumber)

class BorrowerInfo(models.Model):
    loanNumber = models.ForeignKey(
        'LoanRequests',
        on_delete=models.CASCADE,
        )
    firstName = models.CharField(max_length=100,null=True)
    lastName = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName

class LoanInfo(models.Model):
    loanNumber = models.ForeignKey(
        'LoanRequests',
        on_delete=models.CASCADE,
        )
    program = models.CharField(max_length=30,null=True)
    amount = models.FloatField(default=0)
    fico = models.IntegerField(default=0)
    income = models.FloatField(default=0)

class PropertyInfo(models.Model):
    loanNumber = models.ForeignKey(
        'LoanRequests',
        on_delete=models.CASCADE,
        )
    address = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200, default='United States',null=True)
    state = models.CharField(max_length=100,null=True)
    zip = models.CharField(max_length=10,null=True)
