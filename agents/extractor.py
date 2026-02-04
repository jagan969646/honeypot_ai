from utils.regex_patterns import (
    UPI_PATTERN,
    URL_PATTERN,
    BANK_ACC_PATTERN,
    PHONE_PATTERN,
    EMAIL_PATTERN
)

import re
from typing import Dict, List

# ==============================
# REGEX PATTERNS
# ==============================

UPI_PATTERN = r'\b[\w\.-]+@[\w\.-]+\b'
URL_PATTERN = r'https?://[^\s]+'
BANK_ACC_PATTERN = r'\b\d{9,18}\b'
PHONE_PATTERN = r'\b[6-9]\d{9}\b'
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# ==============================
# EXTRACTION FUNCTION
# ==============================

def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract scam intelligence entities from text.
    Returns dictionary of extracted data.
    """

    if not text:
        return {
            "upi": [],
            "links": [],
            "bank": [],
            "phones": [],
            "emails": []
        }

    upi_ids = re.findall(UPI_PATTERN, text)
    urls = re.findall(URL_PATTERN, text)
    bank_accounts = re.findall(BANK_ACC_PATTERN, text)
    phones = re.findall(PHONE_PATTERN, text)
    emails = re.findall(EMAIL_PATTERN, text)

    # Remove duplicates
    upi_ids = list(set(upi_ids))
    urls = list(set(urls))
    bank_accounts = list(set(bank_accounts))
    phones = list(set(phones))
    emails = list(set(emails))

    return {
        "upi": upi_ids,
        "links": urls,
        "bank": bank_accounts,
        "phones": phones,
        "emails": emails
    }
