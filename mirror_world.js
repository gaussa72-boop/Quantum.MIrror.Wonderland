// mirror_world.js - Spiegelhalle mit dynamischen Spiegeln

const MIRRORS_DATA = [
    { id: 1, name: "🎮 Game Creator", color: "#ff1493" },
    { id: 2, name: "🎨 Design Studio", color: "#00ced1" },
    { id: 3, name: "📚 Story Engine", color: "#ffd700" },
    { id: 4, name: "🔮 Dream World", color: "#9370db" },
    { id: 5, name: "⚡ Quantum Lab", color: "#00ff7f" },
    { id: 6, name: "🌌 Cosmos", color: "#ff6347" }
];

class MirrorWorld {
    constructor() {
        this.mirrorContainer = document.getElementById("mirrors");
        this.selectedMirror = null;
        this.initMirrors();
    }

    initMirrors() {
        MIRRORS_DATA.forEach(mirror => {
            const mirrorBtn = document.createElement("div");
            mirrorBtn.className = "mirror-button";
            mirrorBtn.innerHTML = mirror.name;
            mirrorBtn.style.borderColor = mirror.color;
            mirrorBtn.style.boxShadow = `0 0 30px ${mirror.color}, inset 0 0 30px rgba(${this.hexToRgb(mirror.color)}, 0.3)`;

            mirrorBtn.addEventListener("click", () => this.openMirror(mirror));
            mirrorBtn.addEventListener("mouseenter", () => this.mirrorHoverEffect(mirrorBtn, mirror.color));
            mirrorBtn.addEventListener("mouseleave", () => this.resetMirror(mirrorBtn, mirror.color));

            this.mirrorContainer.appendChild(mirrorBtn);
        });
    }

    openMirror(mirror) {
        this.selectedMirror = mirror;
        document.getElementById("chat-abteil").style.display = "flex";
        document.getElementById("cat-speech").innerHTML = `Öffne Spiegel: ${mirror.name}... 🪞✨`;

        // Generiere neue Game/Design für diesen Spiegel
        this.generateGameForMirror(mirror);
    }

    generateGameForMirror(mirror) {
        console.log(`Generiere Game für Spiegel: ${mirror.name}`);
        // Backend-Call würde hier stattfinden
    }

    mirrorHoverEffect(element, color) {
        element.style.boxShadow = `0 0 50px ${color}, inset 0 0 50px rgba(${this.hexToRgb(color)}, 0.5)`;
    }

    resetMirror(element, color) {
        element.style.boxShadow = `0 0 30px ${color}, inset 0 0 30px rgba(${this.hexToRgb(color)}, 0.3)`;
    }

    hexToRgb(hex) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `${r}, ${g}, ${b}`;
    }

    breakMirror(mirrorId) {
        console.log(`Spiegel ${mirrorId} ist zerbrochen! Neue Welt wird erzeugt...`);
        this.regenerateDesign();
    }

    regenerateDesign() {
        document.getElementById("cat-speech").innerHTML = "Die Spiegel zerbrechen! Neue paradiesische Welten entstehen! 🌈✨";
    }
}

// Initialisiere Spiegelhalle
const mirrorWorld = new MirrorWorld();

