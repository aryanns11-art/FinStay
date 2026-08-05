from enum import Enum


class PaymentMethodEnum(str, Enum):
    CASH = "Cash"
    UPI = "UPI"
    BANK = "Bank"
    CARD = "Card"