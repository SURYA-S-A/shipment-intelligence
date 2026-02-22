from enum import Enum


class CommunicationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    CALL = "call"
    TMS_EVENT = "tms_event"
