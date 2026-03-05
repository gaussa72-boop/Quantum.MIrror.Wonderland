// user_avatar.js - User Avatar Management & Evolution

class UserAvatarSystem {
    constructor() {
        this.avatarName = document.getElementById("avatar-name");
        this.evolutionLevel = document.getElementById("evolution-level");
        this.currentUser = {
            id: 1,
            name: "Quantum Wanderer",
            personality: "curious",
            memory: {},
            interactionCount: 0,
            level: 1,
            favoriteGames: []
        };

        this.loadUserProfile();
        this.initAvatarReactions();
    }

    loadUserProfile() {
        // Lade oder erstelle User-Profil
        const stored = localStorage.getItem("quantumUserProfile");
        if (stored) {
            this.currentUser = JSON.parse(stored);
        }
        this.updateAvatarDisplay();
    }

    saveUserProfile() {
        localStorage.setItem("quantumUserProfile", JSON.stringify(this.currentUser));
    }

    updateAvatarDisplay() {
        this.avatarName.textContent = this.currentUser.name;
        this.evolutionLevel.textContent = `Level ${this.currentUser.level}`;
    }

    evolveAvatar() {
        this.currentUser.interactionCount++;

        // Berechne neues Level
        const newLevel = Math.floor(this.currentUser.interactionCount / 10) + 1;
        if (newLevel > this.currentUser.level && newLevel <= 10) {
            this.currentUser.level = newLevel;
            this.handleLevelUp();
        }

        // Passe Persönlichkeit an basierend auf Verhalten
        this.adaptPersonality();
        this.updateAvatarDisplay();
        this.saveUserProfile();
    }

    handleLevelUp() {
        companion.speak(`${this.currentUser.name} ist nun Level ${this.currentUser.level}! 🎉✨`);

        // Neue Fähigkeiten freischalten
        const abilities = {
            2: "Du kannst nun Spiegel schneller öffnen!",
            3: "Du kannst die Singularität manipulieren!",
            4: "Du bekommst Zugang zur Dream World!",
            5: "Du kannst Welten zusammenführen!",
            6: "Du bist nun ein Co-Creator!",
            7: "Du verstehst die Quantenlogik!",
            8: "Du kannst Spiegel heilen!",
            9: "Du bist ein Master of Wonderland!",
            10: "Du bist ein Quantum God! 🌌"
        };

        if (abilities[this.currentUser.level]) {
            companion.speak(abilities[this.currentUser.level]);
        }
    }

    adaptPersonality() {
        const personalities = [
            { level: 1, type: "curious", desc: "Neugierig und entdeckungslustig" },
            { level: 3, type: "brave", desc: "Mutig und abenteuerlustig" },
            { level: 5, type: "wise", desc: "Weise und nachdenklich" },
            { level: 7, type: "mystical", desc: "Mystisch und unendlich" },
            { level: 10, type: "quantum", desc: "Quantenentangled und allwissend" }
        ];

        for (let p of personalities) {
            if (this.currentUser.level >= p.level) {
                this.currentUser.personality = p.type;
            }
        }
    }

    recordGameCreation(gameName, gameType) {
        this.currentUser.favoriteGames.push({
            name: gameName,
            type: gameType,
            createdAt: new Date().toISOString()
        });

        this.evolveAvatar();
        companion.speak(`${this.currentUser.name} hat "${gameName}" erstellt! 🎮✨`);
    }

    recordChatInteraction(message) {
        this.currentUser.memory[`msg_${this.currentUser.interactionCount}`] = message;
        this.evolveAvatar();
    }

    getUserStats() {
        return {
            name: this.currentUser.name,
            level: this.currentUser.level,
            personality: this.currentUser.personality,
            interactions: this.currentUser.interactionCount,
            gamesCreated: this.currentUser.favoriteGames.length,
            memories: Object.keys(this.currentUser.memory).length
        };
    }

    initAvatarReactions() {
        // Avatar reagiert auf verschiedene Events
        window.addEventListener("mirrorOpened", () => {
            companion.speak(`${this.currentUser.name} öffnet einen neuen Spiegel! 🪞`);
        });

        window.addEventListener("mirrorBroken", () => {
            companion.speak(`Ein Spiegel zerbricht! Die Realität splittet sich! 💥`);
        });

        window.addEventListener("gameCreated", (e) => {
            this.recordGameCreation(e.detail.name, e.detail.type);
        });

        window.addEventListener("messageReceived", (e) => {
            this.recordChatInteraction(e.detail.message);
        });
    }

    customizeAvatar(newName) {
        this.currentUser.name = newName;
        this.updateAvatarDisplay();
        this.saveUserProfile();
        companion.speak(`Ah! Du heißt jetzt ${newName}! Angenehm! 🎭`);
    }

    showAvatarStats() {
        const stats = this.getUserStats();
        const statsText = `
            👤 ${stats.name}
            Level: ${stats.level}
            Persönlichkeit: ${stats.personality}
            Interaktionen: ${stats.interactions}
            Spiele erstellt: ${stats.gamesCreated}
            Erinnerungen: ${stats.memories}
        `;

        companion.speak(statsText);
    }

    resetAvatar() {
        if (confirm("Möchtest du dein Avatar-Profil wirklich zurücksetzen?")) {
            localStorage.removeItem("quantumUserProfile");
            location.reload();
        }
    }
}

// Initialisiere Avatar-System
const avatarSystem = new UserAvatarSystem();

// Beispiel: Avatar kustomisieren
function setAvatarName(name) {
    avatarSystem.customizeAvatar(name);
}

// Beispiel: Statistiken anzeigen
function showStats() {
    avatarSystem.showAvatarStats();
}

