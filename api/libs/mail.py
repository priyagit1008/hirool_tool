import logging
import datetime
# django level imports
from django.core.mail import EmailMessage,send_mail

# project imports
from api.settings import EMAIL_HOST_USER


# Third Party Libraries
from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def sendmail(message,subject,tolist):

	# send_mail('otp generating','Registration succesfull','priyapatil1421997@gmail.com',[email],fail_silently=False,)
	try:
		send_mail(subject, message, EMAIL_HOST_USER,tolist)
		logger.info("Mail Sent ")
		return True
	except:
		print ("email not recived")
		logger.error("Sending mail is failed", exc_info=True)
		return False