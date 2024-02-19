from enum import Enum


class Status(Enum):
    NO_REQUEST_SENT = -1
    THEM_SENT_TO_U = 0
    U_SENT_TO_THEM = 1
