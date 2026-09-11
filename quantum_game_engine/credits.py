"""Prepaid credit ledger and payment-provider contracts for Dunkle Spiegel.

The ledger grants credits only after a verified, idempotent payment event.
No cryptocurrency private keys or custody logic belong in this application.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from dataclasses import dataclass
from typing import Any

PACKAGES = {
    "spark": {"name": "Spark", "credits": 100, "price_eur_cents": 999},
    "quantum": {"name": "Quantum", "credits": 550, "price_eur_cents": 3999},
    "ultra": {"name": "Ultra", "credits": 1400, "price_eur_cents": 8999},
    "creator": {"name": "Creator", "credits": 3200, "price_eur_cents": 17999},
}

@dataclass(frozen=True)
class PaymentIntent:
    id: str
    user_id: str
    package_id: str
    provider: str
    amount_eur_cents: int
    credits: int
    status: str = "pending"

class CreditLedger:
    """In-memory reference ledger; production should persist it transactionally in PostgreSQL."""
    def __init__(self) -> None:
        self.balances: dict[str, int] = {}
        self.intents: dict[str, PaymentIntent] = {}
        self.processed_events: set[str] = set()
        self.entries: list[dict[str, Any]] = []

    def balance(self, user_id: str) -> int:
        return self.balances.get(str(user_id), 0)

    def create_intent(self, user_id: str, package_id: str, provider: str) -> PaymentIntent:
        if package_id not in PACKAGES:
            raise ValueError("Unknown credit package.")
        if provider not in {"stripe", "crypto"}:
            raise ValueError("Unsupported payment provider.")
        p = PACKAGES[package_id]
        intent = PaymentIntent(secrets.token_hex(12), str(user_id), package_id, provider, p["price_eur_cents"], p["credits"])
        self.intents[intent.id] = intent
        return intent

    def confirm(self, event_id: str, intent_id: str, provider: str) -> int:
        if not event_id or event_id in self.processed_events:
            return 0
        intent = self.intents.get(intent_id)
        if not intent or intent.provider != provider:
            raise ValueError("Unknown payment intent.")
        self.processed_events.add(event_id)
        self.balances[intent.user_id] = self.balance(intent.user_id) + intent.credits
        self.entries.append({"event_id": event_id, "intent_id": intent.id, "user_id": intent.user_id, "credits": intent.credits, "provider": provider, "timestamp": int(time.time())})
        return intent.credits


def verify_webhook(raw_body: bytes, signature: str, secret: str) -> bool:
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def public_catalog() -> dict[str, dict[str, Any]]:
    return PACKAGES
