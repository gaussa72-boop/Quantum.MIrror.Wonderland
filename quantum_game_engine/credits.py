"""Prepaid credit ledger and payment-provider contracts for Dunkle Spiegel.

The ledger grants credits only after a verified, idempotent payment event.
Generation credits are reserved before generation and consumed only after a
successful project has been generated. Reservations are released on failure.
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
        self.reservations: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()

    def balance(self, user_id: str) -> int:
        with self._lock:
            return self.balances.get(str(user_id), 0)

    def available_balance(self, user_id: str) -> int:
        """Spendable balance after subtracting active generation reservations."""
        user_id = str(user_id)
        with self._lock:
            reserved = sum(r["credits"] for r in self.reservations.values() if r["user_id"] == user_id and r["status"] == "reserved")
            return self.balances.get(user_id, 0) - reserved

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

    def reserve_for_generation(self, user_id: str, kind: str) -> str:
        """Atomically reserve credits so concurrent generations cannot overspend."""
        cost = GENERATION_COSTS.get(kind)
        if cost is None:
            raise ValueError("Unsupported generation type.")
        user_id = str(user_id)
        with self._lock:
            reserved = sum(r["credits"] for r in self.reservations.values() if r["user_id"] == user_id and r["status"] == "reserved")
            current = self.balances.get(user_id, 0)
            available = current - reserved
            if available < cost:
                raise ValueError(f"Insufficient credits: {cost} required, {available} available.")
            reservation_id = secrets.token_hex(12)
            self.reservations[reservation_id] = {"user_id": user_id, "kind": kind, "credits": cost, "status": "reserved", "timestamp": int(time.time())}
            self.entries.append({"reservation_id": reservation_id, "user_id": user_id, "credits": -cost, "kind": kind, "timestamp": int(time.time()), "type": "generation_reservation"})
            return reservation_id

    def finalize_generation(self, reservation_id: str, project_id: str) -> int:
        """Consume an active reservation after successful generation."""
        with self._lock:
            reservation = self.reservations.get(reservation_id)
            if not reservation or reservation["status"] != "reserved":
                raise ValueError("Invalid or already finalized generation reservation.")
            cost = reservation["credits"]
            user_id = reservation["user_id"]
            current = self.balances.get(user_id, 0)
            if current < cost:
                raise ValueError("Credit balance changed unexpectedly.")
            self.balances[user_id] = current - cost
            reservation["status"] = "finalized"
            reservation["project_id"] = str(project_id)
            self.entries.append({"reservation_id": reservation_id, "user_id": user_id, "credits": -cost, "kind": reservation["kind"], "project_id": str(project_id), "timestamp": int(time.time()), "type": "generation"})
            return cost

    def release_generation(self, reservation_id: str) -> int:
        """Release an active reservation when generation fails."""
        with self._lock:
            reservation = self.reservations.get(reservation_id)
            if not reservation or reservation["status"] != "reserved":
                return 0
            reservation["status"] = "released"
            self.entries.append({"reservation_id": reservation_id, "user_id": reservation["user_id"], "credits": reservation["credits"], "kind": reservation["kind"], "timestamp": int(time.time()), "type": "generation_reservation_release"})
            return reservation["credits"]

    def consume_for_generation(self, user_id: str, kind: str, project_id: str) -> int:
        """Backward-compatible atomic charge for callers without an explicit reservation."""
        reservation_id = self.reserve_for_generation(user_id, kind)
        try:
            return self.finalize_generation(reservation_id, project_id)
        except Exception:
            self.release_generation(reservation_id)
            raise

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
