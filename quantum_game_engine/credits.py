"""Prepaid credit ledger and payment-provider contracts for Dunkle Spiegel.

The ledger grants credits only after a verified, idempotent payment event.
Generation credits are consumed only after a project has been generated successfully.
No cryptocurrency private keys or custody logic belong in this application.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
import time
from dataclasses import dataclass
from typing import Any

PACKAGES = {
    "spark": {"name": "Spark", "credits": 100, "price_eur_cents": 999},
    "quantum": {"name": "Quantum", "credits": 550, "price_eur_cents": 3999},
    "ultra": {"name": "Ultra", "credits": 1400, "price_eur_cents": 8999},
    "creator": {"name": "Creator", "credits": 3200, "price_eur_cents": 17999},
}

GENERATION_COSTS = {"game": 25, "dlc": 15, "mod": 10}

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
        self._lock = threading.RLock()

    def balance(self, user_id: str) -> int:
        with self._lock:
            return self.balances.get(str(user_id), 0)

    def create_intent(self, user_id: str, package_id: str, provider: str) -> PaymentIntent:
        if package_id not in PACKAGES:
            raise ValueError("Unknown credit package.")
        if provider not in {"stripe", "crypto"}:
            raise ValueError("Unsupported payment provider.")
        p = PACKAGES[package_id]
        intent = PaymentIntent(secrets.token_hex(12), str(user_id), package_id, provider, p["price_eur_cents"], p["credits"])
        with self._lock:
            self.intents[intent.id] = intent
        return intent

    def confirm(self, event_id: str, intent_id: str, provider: str) -> int:
        if not event_id:
            raise ValueError("event_id is required.")
        with self._lock:
            if event_id in self.processed_events:
                return 0
            intent = self.intents.get(intent_id)
            if not intent or intent.provider != provider:
                raise ValueError("Unknown payment intent.")
            self.processed_events.add(event_id)
            self.balances[intent.user_id] = self.balance(intent.user_id) + intent.credits
            self.entries.append({"event_id": event_id, "intent_id": intent.id, "user_id": intent.user_id, "credits": intent.credits, "provider": provider, "timestamp": int(time.time()), "type": "credit_purchase"})
            return intent.credits

    def consume_for_generation(self, user_id: str, kind: str, project_id: str) -> int:
        """Atomically charge a successful generation. Raises ValueError if funds are insufficient."""
        cost = GENERATION_COSTS.get(kind)
        if cost is None:
            raise ValueError("Unsupported generation type.")
        user_id = str(user_id)
        with self._lock:
            current = self.balances.get(user_id, 0)
            if current < cost:
                raise ValueError(f"Insufficient credits: {cost} required, {current} available.")
            self.balances[user_id] = current - cost
            self.entries.append({"user_id": user_id, "credits": -cost, "kind": kind, "project_id": str(project_id), "timestamp": int(time.time()), "type": "generation"})
            return cost

    def generation_cost(self, kind: str) -> int:
        if kind not in GENERATION_COSTS:
            raise ValueError("Unsupported generation type.")
        return GENERATION_COSTS[kind]


def verify_webhook(raw_body: bytes, signature: str, secret: str) -> bool:
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def public_catalog() -> dict[str, dict[str, Any]]:
    return PACKAGES
