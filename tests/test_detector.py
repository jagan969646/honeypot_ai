from backend.agents.detector import is_scam

def test_scam_message():
    msg = "Earn ₹25,000 per week. Pay ₹1500 registration fee"
    assert is_scam(msg) is True

def test_safe_message():
    msg = "Your bank transaction of ₹500 was successful"
    assert is_scam(msg) is False
