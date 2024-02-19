from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.utils.translation import gettext as _


class GameConsumer(WebsocketConsumer):
    """
    GameConsumer class for websocket connection
    :param WebsocketConsumer: WebsocketConsumer
    :return: None
    """
    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.room_group_name = None
    #     self.room_name = None

    def connect(self):
        """
        :return: None
        """
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        :param close_code: close code
        :return: None
        """
        if close_code == 1006:
            print(_("The connection closed unexpectedly."))
        elif close_code == 1000:
            print(_("Connection closed successfully."))
        else:
            print(_(f"Connection closed. Code: {close_code}"))
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """
        :param text_data: json data
        :param bytes_data: bytes data
        :return: None
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'run_game',
                'payload': text_data
            }
        )

    def send_message(self, text_data):
        """
        :param text_data: json data
        :return: None
        """
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'run_game',
                'payload': text_data
            }
        )

    def run_game(self, event):
        """
        :param event: json data
        :return: None
        """
        data = event['payload']
        data = json.loads(data)

        self.send(text_data=json.dumps({
            'payload': data['data']
        }))
