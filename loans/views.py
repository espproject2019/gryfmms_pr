from django.shortcuts import render
import base64, os
from django.utils import timezone
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document
from app.models import LoanRequests, LoanInfo, BorrowerInfo

from django.http import HttpResponse
import django
from django.conf import settings
from django.core.mail import send_mail


access_token = ''
account_id = ''
file_name_path = 'documents/approval_letter.pdf';
base_path = 'https://demo.docusign.net/restapi'

APP_PATH = os.path.dirname(os.path.abspath(__file__))

# views
def loans(request):
	loans = LoanRequests.objects.all().filter(dateApproved__isnull=True).filter(dateDenied__isnull=True)
	loansList= {'loans': loans}
	return render(request, 'loans/approve.html', loansList)

def submitForApproval(request):
	# all post request data
	data = request.POST.dict()
	# get loanNumber from request
	loanToBeApprovedDenied = data.get('loanNumber')

	# get loan info from database for requested loan
	loan = LoanRequests.objects.all().get(loanNumber=loanToBeApprovedDenied)

	# **** here machine learning results,
	#  should return 1 if loan is approved, 0 if denied
	ml_approved = 1

	# **** end machine learning

	if ml_approved == 1: # if loan is approved
		# update DateApproved in database
		loan.dateApproved=timezone.now()
		loan.save()

		# **** we can put sending email here to Borrower
		# saying that his loan was approved

		# **** end borrower email

		# *** Docusign create envelop and send for e-sign ***
		signer_name = loan.borrower.firstName + ' ' + loan.borrower.lastName
		signer_email = loan.borrower.email

		#email = signer_email
		#data = 'Approved'
		#send_mail('Loan Application', data, "Gryffindors", [email], fail_silently=False)

		# *** calling docusign api
		#results = send_document_for_signing(signer_name, signer_email)
		response = "This loan is approved. Email sent to borrower to e-sign approval letter."
	else: # if loan is denied
		response = "This loan was denied. Email sent to borrower with denial letter."
		# **** we can put sending email here to Borrower
		# saying that his loan was denied

		# **** end borrower email
		#print("\nEnvelope status: " + results.status + ". Envelope ID: " + results.envelope_id + "\n")
	return render(request, 'loans/statusresponse.html', {'response': response})


def send_document_for_signing(signer_name, signer_email):
    """
    Sends the document <file_name> to be signed by <signer_name> via <signer_email>
    """

    # Create the component objects for the envelope definition...
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = Document( # create the DocuSign document object
        document_base64 = base64_file_content,
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model
    signer = Signer( # The signer
        email = signer_email, name = signer_name, recipient_id = "1", routing_order = "1")

    # Create a sign_here tab (field on the document)
    sign_here = SignHere( # DocuSign SignHere field/tab
        document_id = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',
        x_position = '195', y_position = '147')

    # Add the tabs model (including the sign_here tab) to the signer
    signer.tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this Approval Letter for your loan.",
        documents = [document], # The order in the docs array determines the order in the envelope
        recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type
        status = "sent" # requests that the envelope be created and sent.
    )

	# send envelope request
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)
    return results
