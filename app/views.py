from django.shortcuts import render
from django.utils import timezone
from .models import LoanRequests, BorrowerInfo, LoanInfo, PropertyInfo

def home(request):
	return render(request, 'app/home.html')

def apply(request):
	return render(request, 'app/apply.html')

def submitApplication(request):
	# all post request data
	data = request.POST.dict()

	# save to LoanRequest  table
	loan = LoanRequests(
		dateCreated = timezone.now(),
		userID = 123,
	)
	# actual saving
	loan.save()

	# save to BorrowerInfo  table
	borrower = BorrowerInfo(
		loanNumber = loan,
		firstName = data.get('firstName'),
	    lastName = data.get('lastName'),
	    email = data.get('email')
	)
	borrower.save()

	# save to LoanInfo  table
	loanInfo = LoanInfo(
		loanNumber = loan,
		program = data.get('loanprogram'),
	    amount = data.get('loanamount'),
	    fico = data.get('fico'),
	    income = data.get('income')
	)
	loanInfo.save()

	# save to PropertyInfo  table
	propertyinfo = PropertyInfo(
		loanNumber = loan,
		address = data.get('address'),
	    country = data.get('country'),
	    state = data.get('state'),
	    zip = data.get('zip')
	)
	propertyinfo.save()

	return render(request, 'app/apply.html')

def signin(request):
	return render(request, 'app/signin.html')
