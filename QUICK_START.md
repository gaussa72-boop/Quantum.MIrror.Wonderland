# 🌀 QUANTUM MIRROR WONDERLAND - QUICK START GUIDE

## 🚀 Option 1: WEB IM BROWSER (SOFORT)

```bash
# 1. Öffne im Browser:
file:///Users/Querox9396/PycharmProjects/QuantumMirrorWonderland/web/index.html

# Oder starte lokalen Web-Server:
cd /Users/Querox9396/PycharmProjects/QuantumMirrorWonderland/web
python -m http.server 8000

# Dann öffne: http://localhost:8000
```

**Was du siehst:**
- 🐱 Master-Kater oben-links (spricht animiert)
- 🪞 6 bunte Spiegel in der Mitte
- 💬 Chat-Fenster unten-rechts (mit Singularitätssonne)
- 🎨 Meta-Geometrien im Hintergrund

**Zu tun:**
1. Klick auf einen Spiegel (z.B. "Game Creator")
2. Gib eine Idee ein
3. Schreib mit dem Kater im Chat
4. Sieh deinen Avatar evolvieren


---

## 🐳 Option 2: MIT DOCKER (FULL STACK)

```bash
cd /Users/Querox9396/PycharmProjects/QuantumMirrorWonderland

# Starte alle Services:
docker-compose up -d

# Überprüfe Status:
docker-compose ps

# Zugriff auf:
# Web: http://localhost
# Backend API: http://localhost:5000
# PostgreSQL: localhost:5432
# Redis: localhost:6379

# Logs ansehen:
docker-compose logs -f backend

# Alles stoppen:
docker-compose down
```


---

## 🐍 Option 3: PYTHON BACKEND

```bash
cd /Users/Querox9396/PycharmProjects/QuantumMirrorWonderland/backend

# Installiere Dependencies:
pip install -r requirements.txt

# Starte Backend:
python quantum_mirror_backend.py

# Server läuft auf: http://localhost:5000

# In separatem Terminal, starte Web-Server:
cd ../web
python -m http.server 8000

# Öffne: http://localhost:8000
```


---

## 📱 Option 4: IPAD APP

```bash
# Die Swift/SwiftUI Files sind vorbereitet in:
mobile/iPad_Air_App/

# Zum Bauen:
1. Öffne Xcode
2. Create New Project
3. Copy die Files aus iPad_Air_App/
4. Build & Run auf iPad

# Die App verbindet sich mit dem gleichen Backend
```


---

## 🎮 GAMEPLAY TUTORIAL

### 1. ERSTE SCHRITTE
- Master-Kater begrüßt dich
- Dein Avatar wird geladen (oben-rechts)
- Spiegelhalle zeigt 6 Spiegel

### 2. SPIEGEL ÖFFNEN
- Klick auf "Game Creator" Spiegel
- Input-Dialog öffnet sich
- Gib eine Idee ein: "Ich will ein Puzzle-Spiel"
- Enter oder Button klicken

### 3. MIT KATER CHATTEN
- Chat-Fenster öffnet sich unten-rechts
- Gib eine Nachricht ein
- Master-Kater antwortet intelligently
- Deine Interaktionen werden gezählt

### 4. AVATAR EVOLUCIERT
- Jede 10. Interaktion: Level-Up! 🎉
- Neue Fähigkeiten werden freigeschalten
- Persönlichkeit ändert sich (curious → wise → mystical)
- Level anzeige oben-rechts

### 5. SPIEGEL ZERBRECHEN
- Kater kann Spiegel "zerbrechen"
- Neues magisches Design entsteht
- Farben, Formen, Effekte ändern sich
- Neue paradiesische Welt!


---

## 🔧 KONFIGURATION

### Lokale Einstellungen (localStorage)

```javascript
// In Browser Console (F12):

// Avatar-Name ändern:
setAvatarName("Dein Name");

// Statistiken anzeigen:
showStats();

// Avatar zurücksetzen:
avatarSystem.resetAvatar();

// Chat-Raum erstellen:
chat.createGroupChat("Mein Raum");
```

### Backend API Calls

```bash
# Neuen User registrieren:
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"user@example.com"}'

# Chat-Nachricht senden:
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"room":"Wunderland","message":"Hallo Kater!"}'

# Game erstellen:
curl -X POST http://localhost:5000/api/game/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"idea":"Jump and Run Spiel"}'
```


---

## 💻 TECHNISCHE INFOS

### Browser Kompatibilität
- ✅ Chrome 90+
- ✅ Safari 15+
- ✅ Firefox 88+
- ✅ Edge 90+

### Performance
- 60 FPS Animations
- <100ms Response Time
- <50MB Asset Size

### Speicherbedarf
- localStorage: ~1MB pro User
- Browser Cache: ~10MB


---

## 🐛 TROUBLESHOOTING

### Web-Version lädt nicht
```bash
# 1. Check ob Datei existiert:
ls -la web/index.html

# 2. Starte Web-Server:
cd web && python -m http.server 8000

# 3. Öffne: http://localhost:8000
```

### Master-Kater spricht nicht
```javascript
// In Browser Console:
companion.speak("Test!");  // sollte was sagen
```

### Chat-Visualizer funktioniert nicht
```javascript
// Canvas-Fehler? Check Console (F12):
chat.initSingularitySun();
```

### Avatar speichert nicht
```javascript
// localStorage gesperrt? Check:
localStorage.setItem("test", "value");
// Falls Error: Privatmodus ausschalten
```

### Docker funktioniert nicht
```bash
# 1. Docker läuft?
docker ps

# 2. Ports frei?
lsof -i :5000
lsof -i :5432
lsof -i :6379

# 3. Logs checken:
docker-compose logs

# 4. Rebuild:
docker-compose down -v && docker-compose up -d
```


---

## 📚 WEITERE RESSOURCEN

### Dokumentation
- `MEGA_ZIP_SUMMARY.txt` - Vollständige Feature-Übersicht
- `README_QUANTUM_MIRROR_WONDERLAND.md` - Technische Doku

### Code-Struktur
- `web/index.html` - Haupt-UI
- `web/style.css` - Styling & Animations
- `web/mirror_world.js` - Spiegelhalle
- `web/companion_widget.js` - Master-Kater
- `web/chat.js` - Chat-System
- `web/meta_geometry.js` - Geometrien
- `web/user_avatar.js` - Avatar-Evolution
- `backend/quantum_mirror_backend.py` - Backend-Engine

### Community
- GitHub: (wird bereitgestellt)
- Discord: (wird bereitgestellt)
- Twitter: (wird bereitgestellt)


---

## 🎯 NÄCHSTE SCHRITTE

1. **SPIELEN**
   - Öffne Web-Version
   - Erkunde die Spiegelhalle
   - Chatte mit dem Kater

2. **ENTWICKELN**
   - Modifiziere Backend (quantum_mirror_backend.py)
   - Passe Design an (style.css)
   - Füge neue Spiegel hinzu

3. **DEPLOYEN**
   - Docker Compose für lokale Produktion
   - Cloud: Render.com, AWS, Azure
   - Mobile: iPad App bauen

4. **ERWEITERN**
   - Unity 3D Spiegelwelt
   - Voice Integration
   - Multiplayer Chat
   - Custom Games


---

## 📞 SUPPORT

Bei Problemen:

1. **Browser Console (F12)** - Schau auf Fehler
2. **Docker Logs** - `docker-compose logs -f`
3. **Reload** - F5 oder Ctrl+Shift+R
4. **Clear Cache** - localStorage.clear()
5. **Restart Services** - docker-compose restart

---

**Viel Spaß in der Quantum Mirror Wonderland! 🌀✨**

Status: ✅ Ready to Use
Version: 1.0.0
Last Update: March 4, 2026

