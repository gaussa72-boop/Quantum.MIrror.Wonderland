# 📚 GITHUB & RENDER SETUP ANLEITUNG

## 🔧 SCHRITT 1: GitHub Repository erstellen

### A) Repository auf GitHub erstellen
1. Gehe zu [GitHub.com](https://github.com)
2. Klicke "New Repository"
3. Name: `QuantumMirrorWonderland`
4. Description: "A magical KI platform with Master Cat and mirror hall"
5. Public oder Private (empfohlen: Public)
6. Initialisiere NICHT mit README (wir haben schon einen)
7. Klicke "Create repository"

### B) Lokales Git Repository mit GitHub verbinden

```bash
cd /Users/Querox9396/PycharmProjects/QuantumMirrorWonderland

# Initialisiere Git (falls nicht schon geschehen)
git init

# Füge alle Dateien hinzu
git add .

# Erstelle ersten Commit
git commit -m "🌀 Initial commit: Quantum Mirror Wonderland v1.0

- Master-Kater KI-Begleiter
- Spiegelhalle mit 6 Spielen
- Chat-System mit Singularitätssonne
- User Avatar Evolution (10 Levels)
- Heilige Geometrien & Magisches Design
- Multi-Platform (Web/iPad/Unity)
- Production-Ready für Render"

# Verbinde mit GitHub Repository
git remote add origin https://github.com/YOUR_USERNAME/QuantumMirrorWonderland.git

# Benenne main Branch (falls master)
git branch -M main

# Push zum GitHub
git push -u origin main
```

---

## 🚀 SCHRITT 2: Auf Render.com deployen

### A) Render Account erstellen
1. Gehe zu [Render.com](https://render.com)
2. Klicke "Get Started" → "Sign up"
3. Wähle "Sign up with GitHub"
4. Autorisiere GitHub Access

### B) Neuen Web Service auf Render erstellen
1. Auf Render Dashboard → "New +" → "Web Service"
2. Wähle dein GitHub Repository: `QuantumMirrorWonderland`
3. Konfiguriere:
   - **Name:** `quantum-mirror-wonderland`
   - **Environment:** Python 3
   - **Region:** Frankfurt (oder näher zu dir)
   - **Branch:** main
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `gunicorn --chdir . app:app --bind 0.0.0.0:$PORT`

### C) Environment Variables setzen
Auf Render, "Environment" Tab, füge hinzu:

```
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=(wird automatisch generiert)
JWT_SECRET_KEY=(wird automatisch generiert)
DATABASE_URL=sqlite:///quantum_mirror.db
REDIS_URL=redis://localhost:6379/0
```

### D) Deploy starten
1. Klicke "Create Web Service"
2. Warte auf Deployment (2-5 Minuten)
3. Deine App läuft auf: `https://quantum-mirror-wonderland.onrender.com`

---

## 🔗 SCHRITT 3: Auto-Deploy konfigurieren

### GitHub → Render Auto-Push

Jedes Mal, wenn du zu main branch pushst:
```bash
git push origin main
```

Render sieht den Push und deployedt automatisch! 🚀

---

## 🛠 PROBLEMBEHEBUNG

### GitHub Connection fehlgeschlagen?
```bash
# Überprüfe SSH Key
ssh -T git@github.com

# Oder nutze HTTPS statt SSH:
git remote set-url origin https://github.com/YOUR_USERNAME/QuantumMirrorWonderland.git
```

### Render zeigt Fehler?
```bash
# Schaue in Render Logs:
# Dashboard → Service → Logs Tab

# Häufige Fehler:
# - "Module not found" → pip install -r backend/requirements.txt
# - "Port already in use" → Check $PORT env var
# - "Import Error" → Check python path in app.py
```

### App lädt nicht im Browser?
```bash
# Überprüfe ob Backend läuft:
curl https://quantum-mirror-wonderland.onrender.com/health

# Überprüfe Web-Files:
# Render sollte web/ Ordner servieren
```

---

## 📊 RENDER DEPLOYMENT STRUKTUR

Nach dem Deploy hat Render automatisch:

- ✅ **Web Service** mit Gunicorn
- ✅ **Python Environment** mit Dependencies
- ✅ **PostgreSQL** optional (für Production später)
- ✅ **Free HTTPS/SSL** Certificate
- ✅ **Auto-restart** bei Crashes
- ✅ **GitHub Integration** für Auto-Deploy

---

## 🎯 TIPPS FÜR PRODUCTION

### 1. Domain Custom
```
Render Dashboard → Service → Settings
→ Custom Domains
→ Füge deine Domain hinzu (z.B. quantummirror.dev)
```

### 2. Monitoring aktivieren
```
Settings → Alerts
→ Enable alerts für:
  - Service crashes
  - High memory usage
  - High CPU usage
```

### 3. Backup & Restore
```
Falls PostgreSQL später:
Settings → Backup & Restore
→ Auto-backups aktivieren
```

### 4. Performance
```
Settings → Plan
→ Wechsel zu "Standard" Plan für Production
→ Auto-scaling aktivieren
```

---

## 📱 GITHUB PAGES OPTIONAL (für statische Docs)

Falls du möchtest, dass Dokumentation auch auf GitHub Pages sichtbar ist:

```bash
# In Settings → Pages
# Source: main branch /docs folder
# URL: https://YOUR_USERNAME.github.io/QuantumMirrorWonderland
```

---

## ✅ FINAL CHECKLIST

- [ ] GitHub Repository erstellt
- [ ] Lokales Git initialisiert
- [ ] Alle Dateien committed & gepusht
- [ ] Render Account erstellt
- [ ] Web Service auf Render deployed
- [ ] Environment Variables gesetzt
- [ ] Health Check erfolgreich: `/health`
- [ ] Web-Interface lädt: `/`
- [ ] API funktioniert: `/api/companion/speak`
- [ ] Master-Kater spricht
- [ ] Spiegelhalle sichtbar

---

## 🎉 FERTIG!

Deine **Quantum Mirror Wonderland** läuft jetzt auf:

```
🌐 https://quantum-mirror-wonderland.onrender.com
```

Jedes Update auf GitHub deployedt automatisch! 🚀

---

**Weitere Commands:**

```bash
# Logs anschauen
git log --oneline

# Status überprüfen
git status

# Neuen Branch für Features
git checkout -b feature/amazing-feature

# Push nach Feature
git add .
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Pull Request auf GitHub erstellen & mergen
```

---

**Support:** Render Dokumentation → https://render.com/docs

