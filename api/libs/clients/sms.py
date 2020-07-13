from .base_client import BaseClient
from django.conf import settings


class SmsClient(BaseClient):
    """
    """
    def __init__(self, host=settings.SMS_CONFIG['HOST']):
        """
        """
        super().__init__(host)

    def send_sms(self, mobile, message):
        """
        Success Response: '100 - Msg successfully sent. MsgID#35371524'

        Failure Response: '105 - Invalid mobile number provided. Error Nos:807320110,'
        (or something similar to this)
        """
        params = settings.SMS_CONFIG['PARAMS']

        params.update(
                {
                    settings.SMS_CONFIG['SEND_TO_KEYWORD']: mobile,
                    'msg': message,
                }
        )

        url = settings.SMS_CONFIG['URL']
        response = self.get(url_path=url, params=params)

        sent = False
        if response.split(" ")[0] in settings.SMS_CONFIG['SUCCESS_KEYWORD']:
            sent = True
        return (sent, response)
