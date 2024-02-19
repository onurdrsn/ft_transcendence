from django.utils.translation import gettext_lazy as _


class ClientError(Exception):
    """
        Custom exception class that is caught by the websocket receive()
        handler and translated into a send back to the client.
    """
    def __init__(self, code, message=None):
        super().__init__(code, message)
        self.code = code
        self.message = message

    def __str__(self):
        return _(f'ClientError(code = {self.code}, message =  {self.message})')
