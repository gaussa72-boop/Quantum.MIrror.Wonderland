import json
import hashlib
import hmac
from quantum_game_engine.credits import CreditLedger, verify_webhook


def test_credit_grant_is_idempotent():
    ledger = CreditLedger()
    intent = ledger.create_intent('u1', 'spark', 'crypto')
    assert ledger.confirm('evt1', intent.id, 'crypto') == 100
    assert ledger.confirm('evt1', intent.id, 'crypto') == 0
    assert ledger.balance('u1') == 100


def test_webhook_signature():
    body = json.dumps({'status': 'paid'}).encode()
    secret = 'test-secret'
    sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_webhook(body, sig, secret)
    assert not verify_webhook(body, 'bad', secret)
