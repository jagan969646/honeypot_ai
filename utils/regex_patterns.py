# ==============================
# UPI ID PATTERN
# Examples:
# abc@okaxis
# name123@ybl
# ==============================
UPI_PATTERN = r'\b[\w\.-]+@[\w\.-]+\b'


# ==============================
# URL / PHISHING LINK PATTERN
# Examples:
# http://fake.com
# https://bank.verify-now.in
# ==============================
URL_PATTERN = r'https?://[^\s]+'


# ==============================
# BANK ACCOUNT NUMBER
# 9–18 digits
# ==============================
BANK_ACC_PATTERN = r'\b\d{9,18}\b'


# ==============================
# PHONE NUMBER (India Focused)
# Starts 6–9, total 10 digits
# ==============================
PHONE_PATTERN = r'\b[6-9]\d{9}\b'


# ==============================
# EMAIL ID
# ==============================
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'


# ==============================
# OTP CODE
# 4–8 digits
# ==============================
OTP_PATTERN = r'\b\d{4,8}\b'


# ==============================
# IFSC CODE (India Banks)
# Example: HDFC0001234
# ==============================
IFSC_PATTERN = r'\b[A-Z]{4}0[A-Z0-9]{6}\b'
