import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext


def isnt_totally_dumb_password(value):
    digit_pattern = r"\d+"
    symbol_pattern = r"(?=[ -~])(?=[^a-zA-Z0-9])"
    if (not re.search(digit_pattern, value)
            or not re.search(symbol_pattern, value)):
        raise (ValidationError(
               ugettext("This value is too weak to be used as a password.")))
