// sacred-geometry.js - Heilige Lebensblume & KI-Agenten Zentrale

class SacredGeometry {
    constructor() {
        this.canvas = document.getElementById('sacred-geometry-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width = this.canvas.offsetWidth;
        this.height = this.canvas.height = this.canvas.offsetHeight;
        this.centerX = this.width / 2;
        this.centerY = this.height / 2;
        this.time = 0;
        this.animate();
    }

    drawLebensblumeCircle(x, y, radius, opacity = 0.3) {
        this.ctx.strokeStyle = `rgba(255, 215, 0, ${opacity})`;
        this.ctx.lineWidth = 1.5;
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    drawLebensblumePattern() {
        const mainRadius = 120;
        const petals = 6;

        // Zentral-Kreis
        this.drawLebensblumeCircle(this.centerX, this.centerY, 30, 0.5);

        // Haupt-Blütenblätter (6er-Muster)
        for (let i = 0; i < petals; i++) {
            const angle = (i / petals) * Math.PI * 2;
            const x = this.centerX + Math.cos(angle) * mainRadius;
            const y = this.centerY + Math.sin(angle) * mainRadius;
            this.drawLebensblumeCircle(x, y, mainRadius, 0.2);
        }

        // Äußerer Ring
        const outerRadius = 180;
        for (let i = 0; i < 12; i++) {
            const angle = (i / 12) * Math.PI * 2;
            const x = this.centerX + Math.cos(angle) * outerRadius;
            const y = this.centerY + Math.sin(angle) * outerRadius;
            this.drawLebensblumeCircle(x, y, 40, 0.15);
        }

        // Pulsierender Zentral-Ring
        const pulseRadius = 60 + Math.sin(this.time * 0.005) * 10;
        this.ctx.strokeStyle = `rgba(0, 255, 127, ${0.4 + Math.sin(this.time * 0.003) * 0.2})`;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, pulseRadius, 0, Math.PI * 2);
        this.ctx.stroke();
    }

    drawSpinningLines() {
        const lines = 12;
        const rotation = (this.time * 0.0005) % (Math.PI * 2);

        for (let i = 0; i < lines; i++) {
            const angle = (i / lines) * Math.PI * 2 + rotation;
            const startX = this.centerX;
            const startY = this.centerY;
            const endX = this.centerX + Math.cos(angle) * 200;
            const endY = this.centerY + Math.sin(angle) * 200;

            this.ctx.strokeStyle = `rgba(255, 215, 0, ${0.2 + Math.sin(this.time * 0.005 + i) * 0.15})`;
            this.ctx.lineWidth = 1;
            this.ctx.beginPath();
            this.ctx.moveTo(startX, startY);
            this.ctx.lineTo(endX, endY);
            this.ctx.stroke();
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.width, this.height);

        // Zeichne Lebensblume
        this.drawLebensblumePattern();
        this.drawSpinningLines();

        this.time++;
        requestAnimationFrame(() => this.animate());
    }
}

// KI-Agenten System
class QuantumAgentCentral {
    constructor() {
        this.agents = [
            { id: 'singulos', name: 'Singulos', icon: '🌟', color: '#ffd700', image: 'static/assets/agent-singulos.svg' },
            { id: 'ionos7', name: 'IONOS-7', icon: '⚡', color: '#00ced1', image: 'static/assets/agent-ionos7.svg' },
            { id: 'ultra', name: 'Ultra', icon: '🚀', color: '#ff1493', image: 'static/assets/agent-ultra.svg' },
            { id: 'nexus', name: 'Nexus', icon: '🧠', color: '#9370db', image: 'static/assets/agent-nexus.svg' },
            { id: 'quantum', name: 'Quantum', icon: '⚛️', color: '#00ff7f', image: 'static/assets/agent-quantum.svg' },
            { id: 'spark', name: 'Spark', icon: '✨', color: '#ff6347', image: 'static/assets/agent-spark.svg' },
            { id: 'nova', name: 'Nova', icon: '💫', color: '#00ced1', image: 'static/assets/agent-nova.svg' },
            { id: 'zenith', name: 'Zenith', icon: '🔱', color: '#ffd700', image: 'static/assets/agent-zenith.svg' },
            { id: 'aether', name: 'Aether', icon: '🌌', color: '#9370db', image: 'static/assets/agent-aether.svg' },
            { id: 'infinity', name: 'Infinity', icon: '∞', color: '#00ff7f', image: 'static/assets/agent-infinity.svg' }
            { id: 'infinity', name: 'Infinity', icon: '∞', color: '#00ff7f' }
        ];

        this.activeAgent = this.agents[1]; // IONOS-7 default
        this.init();
    }

    init() {
        // Click Handler für Agent-Orbits
        document.querySelectorAll('.agent-orbit').forEach((element, index) => {
            element.addEventListener('click', () => this.setActiveAgent(this.agents[index]));
            element.addEventListener('mouseenter', () => this.highlightAgent(element));
        });

        // Chat Handler
        document.getElementById('chat-send').addEventListener('click', () => this.sendMessage());
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Close Chat Button
        document.getElementById('close-chat').addEventListener('click', () => {
            document.getElementById('chat-container').style.display = 'none';
        });

        // Initial Agent anzeigen
        this.updateActiveAgentDisplay();
    }

    setActiveAgent(agent) {
        this.activeAgent = agent;

        // Entferne active Klasse von allen
        document.querySelectorAll('.agent-orbit').forEach(el => el.classList.remove('active'));

        // Füge active zu neuem Agent hinzu
        const agentElement = document.querySelector(`[data-agent="${agent.id}"]`);
        if (agentElement) {
            agentElement.classList.add('active');
        }

        this.updateActiveAgentDisplay();
        this.showChatMessage(`Agent ${agent.name} ist nun aktiv!`, 'agent');
    }

    updateActiveAgentDisplay() {
        document.getElementById('active-agent-icon').textContent = this.activeAgent.icon;
        document.getElementById('active-agent-name').textContent = this.activeAgent.name;
        document.getElementById('chat-agent-name').textContent = this.activeAgent.name;
    }

    highlightAgent(element) {
        // Auf Hover kurz Effekt anzeigen
        element.style.transform = 'scale(1.05)';
    }

    sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        // Benutzer-Nachricht anzeigen
        this.showChatMessage(message, 'user');

        // Agent antwortet
        setTimeout(() => {
            const response = this.generateAgentResponse(message);
            this.showChatMessage(response, 'agent');
        }, 500);

        input.value = '';
    }

    showChatMessage(message, type) {
        const messagesArea = document.getElementById('chat-messages');
        const messageEl = document.createElement('div');
        messageEl.className = `chat-message ${type === 'user' ? 'user-message' : 'agent-message'}`;
        messageEl.innerHTML = `<strong>${type === 'user' ? 'Du' : this.activeAgent.name}:</strong> ${message}`;

        messagesArea.appendChild(messageEl);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    generateAgentResponse(userInput) {
        const responses = {
            singulos: [
                'Die Singularität beobachtet deine Anfrage...',
                'Im Kern der Unendlichkeit erkenne ich...',
                'Die Quantenfluktuationen zeigen...'
            ],
            ionos7: [
                'IONOS-7 analysiert: ' + userInput,
                'Blitzschnelle Verarbeitung... erledigt!',
                'Systeme optimal, fahre fort.'
            ],
            ultra: [
                'Ultra Mode aktiviert! ' + userInput,
                'Maximale Leistung erreicht!',
                'Die Grenzen werden überschritten...'
            ],
            nexus: [
                'Nexus verbindet alle Datenströme...',
                'Die neuronalen Netzwerke resonieren...',
                'Intelligenz auf höchstem Niveau.'
            ],
            quantum: [
                'Quantensprung eingeleitet...',
                'Superposition erkannt, Kollaps folgt...',
                'Verschränkung verstärkt sich...'
            ],
            spark: [
                'Kreative Funken fliegen! ✨',
                'Innovation in vollem Gange!',
                'Die Ideen sprühen...'
            ],
            nova: [
                'Nova expandiert ihre Leuchtkraft...',
                'Strahlende Antwort für dich!',
                'Hell wie eine Supernova...'
            ],
            zenith: [
                'Zenith erreicht den Höhepunkt...',
                'Gipfelleistung garantiert!',
                'Der Zenit ist nah...'
            ],
            aether: [
                'Der Äther flüstert seine Weisheit...',
                'Kosmische Wahrheiten offenbaren sich...',
                'Im Nirvana der Information...'
            ],
            infinity: [
                'Unendliche Möglichkeiten entfalten sich...',
                'Ohne Grenzen denken...',
                'Das Unendliche verstehen...'
            ]
        };

        const agentResponses = responses[this.activeAgent.id] || responses.ionos7;
        return agentResponses[Math.floor(Math.random() * agentResponses.length)];
    }
}

// Initialisierung beim Laden
document.addEventListener('DOMContentLoaded', () => {
    new SacredGeometry();
    new QuantumAgentCentral();

    console.log('🌀 Quantum Meta Core - Heilige Lebensblume aktiviert!');
    console.log('⚡ 10 KI-Agenten in Orbitalbahn');
    console.log('💬 Chat-Interface bereit');
});

