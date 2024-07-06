from decimal import Decimal
import re

def extract_amount_from_mpesa(message):
    match = re.search(r'Ksh\s*([\d,]+(?:\.\d{2})?)\s*sent', message)
    if match:
        return Decimal(match.group(1).replace(',', ''))
    return None