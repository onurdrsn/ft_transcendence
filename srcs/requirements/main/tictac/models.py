from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_room_code(value):
    if not value.isascii() or not value.isalnum() or len(value) >= 100:
        raise ValidationError("Invalid room code")


class TicTacToe(models.Model):
    room_code = models.CharField(max_length=100, validators=[validate_room_code])
    game_creator = models.CharField(max_length=100)
    game_opponent = models.CharField(max_length=100, blank=True, null=True)
    is_over = models.BooleanField(default=False)
    winner = models.CharField(max_length=100, blank=True, null=True)
    dated = models.DateTimeField(default=timezone.now)

    def player_count(self):
        count = 0
        if self.game_creator:
            count += 1
        if self.game_opponent:
            count += 1
        return count
