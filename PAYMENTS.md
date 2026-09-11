# Dunkle Spiegel — Credits & Payments

## Modell

Dunkle Spiegel verwendet **vorausbezahlte Credits** für KI-Generierungen. Die Anwendung kennt nur Credit-Guthaben und Zahlungsereignisse; sie verwahrt keine Krypto-Private-Keys.

### Pakete

- Spark — 100 Credits — 9,99 €
- Quantum — 550 Credits — 39,99 €
- Ultra — 1.400 Credits — 89,99 €
- Creator — 3.200 Credits — 179,99 €

## Provider

Die Architektur unterstützt `stripe` und `crypto` als Provider. Der aktuelle Code erzeugt Zahlungs-Intents und akzeptiert nur signierte, als `paid` bestätigte Webhook-Ereignisse. Doppelte Events werden anhand der Event-ID nicht erneut gutgeschrieben.

Für eine echte Vermarktung müssen die Provider-Checkout-Flows und deren offizielle Webhooks angeschlossen werden. Es dürfen niemals Private Keys oder Seed Phrases im Repository oder auf dem Game-Server liegen.

## Produktion

Vor Live-Verkauf ergänzen:

1. PostgreSQL-Transaktionen für Ledger, Kunden, Orders und Refunds.
2. Offizielle Stripe-Webhooks mit deren Signaturprüfung.
3. Einen regulierten Crypto-Payment-Provider statt eigener Wallet-Custody.
4. Rechnungen, Steuer-/Umsatzsteuerlogik, Widerruf/Erstattung, AGB, Datenschutz und Impressum.
5. Betrugs-/Chargeback-Handling und Audit-Logs.
6. Authentifizierte Benutzer statt `guest`-Konten.
7. Credit-Verbrauch als atomische Ledger-Buchung mit ausreichendem Guthaben.

Der vorhandene `CreditLedger` ist daher ein **sicheres Integrations-Grundgerüst**, aber noch kein vollständiges Produktions-Billing-System.
