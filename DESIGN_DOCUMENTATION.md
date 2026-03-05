╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🎨 QUANTUM META CORE - APP-DESIGN DOKUMENTATION 🎨            ║
║                                                                            ║
║                  Heilige Lebensblume mit KI-Agenten Zentrale              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


📖 DESIGN-ÜBERSICHT
═════════════════════════════════════════════════════════════════════════════

PROJEKT: Quantum Meta Core v2.0
DESIGN: Sacred Geometry with Orbiting AI Agents
DATEIFORMAT: HTML5 + CSS3 + Vanilla JavaScript
KOMPATIBILITÄT: Alle modernen Browser (Chrome, Safari, Firefox, Edge)


🎯 VISUELLE ARCHITEKTUR
═════════════════════════════════════════════════════════════════════════════

[LAYER 1: HEILIGE LEBENSBLUME - ZENTRUM]
├─ Position: Fixed, 50% 50% (absolutes Zentrum)
├─ Size: 600x600px (responsive auf kleinere Screens)
├─ Canvas-basiert für Performance
├─ Elemente:
│  ├─ Zentral-Kreis (30px Radius, pulsierend)
│  ├─ 6 Blütenblätter (120px Radius)
│  ├─ 12 äußere Kreise (180px Radius)
│  ├─ Spinning Lines (12 rotierende Linien)
│  └─ Outer-Ring (pulsierend mit Sinus-Kurve)
├─ Farben: Gold (#ffd700) mit Alpha-Variationen
└─ Update-Rate: Jedes Frame (60 FPS)

[LAYER 2: KI-AGENTEN ORBITALBAHN]
├─ Position: Fixed, um Zentrum
├─ Size: 800x800px Container
├─ 10 Agent-Elemente kreisen
├─ Orbit-Radius: 350px
├─ Rotation: 30 Sekunden pro Umrundung
├─ Staggered Animation (jeder Agent -3s Delay)
├─ Elemente pro Agent:
│  ├─ Kreis (100x100px, border-radius 50%)
│  ├─ Icon (Emoji, 2.5em)
│  ├─ Name (0.7em, Gold Text-Shadow)
│  └─ Border (3px Cyan, Glow-Effekt)
└─ Interaktiv:
   ├─ Hover: scale(1.2), Cyan Glow
   ├─ Active: Grün Glow (#00ff7f), Green Border
   └─ Click: Aktiviert Agent, wechselt Chat-Partner

[LAYER 3: AKTIVER AGENT DISPLAY]
├─ Position: Fixed Zentrum (über Lebensblume)
├─ Size: Dynamisch (330x220px padding)
├─ Hintergrund: Glass-Effekt (backdrop-filter blur(10px))
├─ Border: 2px Gold mit Glow
├─ Elemente:
│  ├─ Icon (4em, animiert pulsing 2s)
│  ├─ Name (2em, Gold, Text-Shadow)
│  └─ Status (0.9em, Lime Green, blinking 1.5s)
└─ Update: Echtzeit auf Agent-Wechsel

[LAYER 4: CHAT-INTERFACE]
├─ Position: Fixed Bottom-Right (30px Offset)
├─ Size: 420x550px (responsive auf Mobile)
├─ Hintergrund: Semi-transparent (rgba(10,10,26,0.85))
├─ Effekt: Glaseffekt (backdrop-filter blur(20px))
├─ Border: 2px Gold mit Glow-Shadow
├─ Z-Index: 50 (über allem)
├─ Struktur:
│  ├─ Header (20px padding, Gold Bottom-Border)
│  │  ├─ Chat-Titel (Agent-Name)
│  │  ├─ Status-Indicator (Grün, pulsing)
│  │  └─ Close-Button (× mit Hover-Effekt)
│  ├─ Messages-Area (flex: 1, overflow-y auto)
│  │  ├─ User-Messages: Cyan, rechts-aligned
│  │  ├─ Agent-Messages: Gold, links-aligned
│  │  └─ Slide-In Animation (0.3s)
│  ├─ Input-Area
│  │  ├─ Input-Feld (Cyan Border, Focus-Glow)
│  │  └─ Send-Button (Gradient Gold-Red, Hover-Scale)
│  └─ Scrollbar: Gold (hover → Cyan)
└─ Interaktivität:
   ├─ Auto-Scroll bei neuen Messages
   ├─ Enter-Key Send
   ├─ Click Send-Button
   └─ Close-Button versteckt Interface

[LAYER 5: INFO PANEL]
├─ Position: Fixed Top-Left (20px Offset)
├─ Background: Semi-transparent Gold (rgba(255,215,0,0.1))
├─ Border: 2px Gold, Border-Radius 15px
├─ Inhalt:
│  ├─ Title: "Quantum Meta Core"
│  ├─ Subtitle: "KI-Agenten Zentrale"
│  └─ Count: "10 Agenten online" (pulsing)
└─ Z-Index: 30


🎯 FARBPALETTE
═════════════════════════════════════════════════════════════════════════════

PRIMARY COLORS:
├─ Gold: #ffd700 (Lebensblume, Buttons, Borders, Text)
├─ Cyan: #00ced1 (Secondary, Hover-Effects, Agent-Borders)
└─ Lime Green: #00ff7f (Active-State, Status, Success)

SECONDARY COLORS:
├─ Hot Pink: #ff1493 (Accent, Alt-Hover)
├─ Red: #ff6347 (Energy, Button-Gradient)
├─ Purple: #9370db (Mystique, Alt-Agents)
└─ Dark Blue: #0a0a1a (Background Gradient)

BACKGROUND:
├─ Radial-Gradient: #0a0a1a (center) → #000000 (edges)
└─ No additional images (Canvas-basiert für Performance)


🎬 ANIMATIONEN & TRANSITIONS
═════════════════════════════════════════════════════════════════════════════

LEBENSBLUME:
├─ @keyframes orbit (360deg rotation, 30s loop)
├─ Pulsing Zentral-Ring (Sinus-Kurve, realtime)
├─ Spinning Lines (Canvas-Rotation, 0.0005 rad/frame)
├─ Opacity-Variation für Tiefe
└─ 60 FPS Canvas-Rendering

AGENTEN:
├─ @keyframes orbit (30s linear, staggered delays)
├─ Hover: transform scale(1.2) + Glow (0.3s transition)
├─ Active: Background-Gradient-Change + Glow-Box-Shadow
├─ Smooth Color-Transitions (0.3s)
└─ Click-Animation: Instant Active-State

CHAT-MESSAGES:
├─ @keyframes slideIn (0.3s ease-out)
├─ Nachricht erscheint von oben
├─ Auto-Scroll auf neue Messages
└─ Fade & Move simultaneously

UI-ELEMENTE:
├─ @keyframes pulse (2s ease-in-out)
│  └─ Icon im Active-Agent-Display
├─ @keyframes blink (1.5s ease-in-out)
│  └─ Status-Text ("Online")
├─ @keyframes pulse-dot (1.5s ease-in-out)
│  └─ Status-Indicator im Chat-Header
└─ @keyframes pulse-text (2s ease-in-out)
   └─ Info-Panel Text

HOVER & TRANSITIONS:
├─ Smooth Color-Changes (0.3s transition)
├─ Scale-Transforms (0.3s transition)
├─ Button-Effects (click: scale(0.95), hover: scale(1.1))
└─ Input-Focus-Glow (0.3s, border-color + box-shadow)


💻 RESPONSIVE DESIGN
═════════════════════════════════════════════════════════════════════════════

BREAKPOINT 1: Desktop (>1024px)
├─ Sacred-Geometry: 600x600px
├─ Agents-Orbit: 800x800px, Orbit-Radius 350px
├─ Agent-Size: 100x100px
├─ Chat-Interface: 420x550px
├─ Info-Panel: Standard
└─ Vollständiger Layout

BREAKPOINT 2: Tablet (1024px - 768px)
├─ Sacred-Geometry: 500x500px
├─ Agents-Orbit: 600x600px, Orbit-Radius 250px
├─ Agent-Size: 80x80px
├─ Chat-Interface: 380x480px
├─ Info-Panel: Verkleint
└─ Angepasst für kleinere Bildschirme

BREAKPOINT 3: Mobile (<768px)
├─ Sacred-Geometry: 300x300px
├─ Agents-Orbit: 400x400px, Orbit-Radius 150px
├─ Agent-Size: 70x70px
├─ Chat-Interface: 90vw (Full-Width) + 70vh (Height)
├─ Info-Panel: Minimiert
├─ Font-Sizes: Reduziert
└─ Touch-optimiert


📁 DATEISTRUKTUR
═════════════════════════════════════════════════════════════════════════════

web/
├── index.html
│   ├─ DOCTYPE html
│   ├─ Meta (charset, viewport)
│   ├─ Link zu style.css
│   ├─ Sacred-Geometry-Container (Canvas)
│   ├─ Agents-Orbit-Container (10 Agent-Divs)
│   ├─ Active-Agent-Display
│   ├─ Chat-Interface
│   ├─ Info-Panel
│   └─ Script: app.js
│
├── style.css
│   ├─ Global Styles (* reset)
│   ├─ Body Background (Radial-Gradient)
│   ├─ Sacred-Geometry-Styling
│   ├─ Agent-Orbit-Styling (positions, animations)
│   ├─ Agent-Avatar-Styling (colors, effects)
│   ├─ Active-Agent-Display
│   ├─ Chat-Interface (Glass-Effect)
│   ├─ Chat-Header, Messages, Input
│   ├─ Info-Panel
│   ├─ @keyframes (alle Animationen)
│   └─ @media Queries (Responsive)
│
└── app.js
    ├─ SacredGeometry Klasse
    │   ├─ constructor(canvas, context)
    │   ├─ drawLebensblumePattern()
    │   ├─ drawSpinningLines()
    │   └─ animate() (requestAnimationFrame loop)
    │
    ├─ QuantumAgentCentral Klasse
    │   ├─ agents[] Array (10 Agenten)
    │   ├─ activeAgent (aktuell selektiert)
    │   ├─ init() (Event-Listener)
    │   ├─ setActiveAgent(agent)
    │   ├─ updateActiveAgentDisplay()
    │   ├─ sendMessage()
    │   ├─ showChatMessage(message, type)
    │   └─ generateAgentResponse(input)
    │
    └─ DOMContentLoaded Event
        ├─ new SacredGeometry()
        ├─ new QuantumAgentCentral()
        └─ Console Log


🔄 INTERAKTIONS-FLOW
═════════════════════════════════════════════════════════════════════════════

1. USER LOADS PAGE
   └─ SacredGeometry begins Canvas animation
   └─ 10 Agents begin Orbit animation
   └─ IONOS-7 ist aktiv (default)

2. USER HOVERS OVER AGENT
   └─ Agent-Avatar scale(1.2)
   └─ Glow intensifies

3. USER CLICKS ON AGENT
   └─ setActiveAgent(selectedAgent)
   └─ Alte Agent entfernt Active-Klasse
   └─ Neue Agent erhält Active-Klasse (Grün-Glow)
   └─ updateActiveAgentDisplay() zeigt neuen Agent
   └─ Chat-Title aktualisiert sich
   └─ System-Message: "Agent [Name] ist nun aktiv!"

4. USER TYPES IN CHAT
   └─ Input-Feld updated (Cyan-Border bei Focus)

5. USER SENDS MESSAGE (Enter oder Button-Click)
   └─ showChatMessage(userInput, 'user')
   └─ Message erscheint mit slideIn-Animation
   └─ Auto-Scroll zu neuer Message
   └─ Input-Feld wird geleert

6. AGENT RESPONDS
   └─ setTimeout 500ms (für Realismus)
   └─ generateAgentResponse(input) wählt zufällig
   └─ showChatMessage(response, 'agent')
   └─ Message erscheint mit Slide-In
   └─ Auto-Scroll

7. REPEAT
   └─ User kann mit neuem Agent chatten
   └─ Oder neuer Agent wählen


📊 PERFORMANCE OPTIMIERUNGEN
═════════════════════════════════════════════════════════════════════════════

Canvas Rendering:
├─ requestAnimationFrame für 60 FPS
├─ Nur Lebensblume (no heavy DOM manipulation)
├─ clearRect vor jedem Frame
└─ Minimale Math-Operations pro Frame

CSS Animationen:
├─ @keyframes für Orbit (GPU-accelerated)
├─ transform & opacity nur (beste Performance)
├─ Keine width/height Changes in Animationen
└─ transition für Hover (smooth)

DOM Optimierungen:
├─ Keine dynamische Agent-Erstellung
├─ Feste HTML-Struktur
├─ Event-Delegation wo möglich
├─ classList statt class manipulation
└─ Minimal Reflows/Repaints

Memory Management:
├─ Keine Memory Leaks (Event-Listener sind gebunden)
├─ Canvas wird nicht re-created
├─ Message-Container hat max-height mit overflow
└─ Keine großen Arrays


🎮 BEISPIEL INTERAKTION
═════════════════════════════════════════════════════════════════════════════

User: "Hallo IONOS-7!"
IONOS-7: "IONOS-7 analysiert: Hallo IONOS-7!
Bot: Blitzschnelle Verarbeitung... erledigt!"

User: "Wechsel zu Ultra"
(klickt auf Ultra Agent)
Ultra: "Ultra Mode aktiviert!"
(Chat-Header zeigt "Ultra")
(Ultra Agent hat Grün-Glow)

User: "Was kannst du machen?"
Ultra: "Ultra Mode aktiviert! Was kannst du machen?
Bot: Maximale Leistung erreicht!"


═════════════════════════════════════════════════════════════════════════════

                       🎨 DESIGN DOKUMENTATION 🎨

              Quantum Meta Core v2.0 - Sacred Geometry Edition

        Heilige Lebensblume | 10 KI-Agenten | Chat-Interface
        Glass-Effekt | Gold & Cyan | 60 FPS Animations

                    OPEN: web/index.html

═════════════════════════════════════════════════════════════════════════════

Version: 2.0
Status: ✅ PRODUCTION READY
Performance: ⚡ OPTIMIZED (60 FPS)
Quality: 🌟 PREMIUM UI/UX

