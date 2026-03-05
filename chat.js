// chat.js - Chat-System mit Master-Kater Integration

class ChatSystem {
    constructor() {
        this.chatInput = document.getElementById("chat-input");
        this.chatSend = document.getElementById("chat-send");
        this.chatMessages = document.getElementById("chat-messages");
        this.closeChat = document.getElementById("close-chat");
        this.currentRoom = "Wunderland";
        this.messages = [];
        this.userId = 1; // Placeholder

        this.initEventListeners();
        this.initSingularitySun();
    }

    initEventListeners() {
        this.chatSend.addEventListener("click", () => this.sendMessage());
        this.chatInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") this.sendMessage();
        });
        this.closeChat.addEventListener("click", () => this.closeChartWindow());
    }

    sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        // User Nachricht anzeigen
        this.displayMessage("User", message, "user-message");

        // Kater antwortet
        setTimeout(() => {
            const response = companion.respondToUserInput(message, "Avatar");
            this.displayMessage("Master Kater 🐱", response, "cat-message");

            // Trainiere KI mit dieser Interaktion
            this.storeTrainingData(message, response);

            // Update Evolution Level
            this.updateEvolutionLevel();
        }, 500);

        this.chatInput.value = "";
    }

    displayMessage(sender, text, className) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `chat-message ${className}`;
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;

        this.chatMessages.appendChild(msgDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

        this.messages.push({
            sender,
            text,
            timestamp: new Date().toISOString()
        });
    }

    closeChartWindow() {
        document.getElementById("chat-abteil").style.display = "none";
    }

    storeTrainingData(input, response) {
        // Speichere für Backend-Training
        const trainingEntry = {
            userId: this.userId,
            input,
            response,
            timestamp: new Date().toISOString(),
            room: this.currentRoom
        };

        console.log("Training Data:", trainingEntry);
        // Hier würde Backend-Call stattfinden
    }

    updateEvolutionLevel() {
        const level = Math.ceil(this.messages.length / 10);
        document.getElementById("evolution-level").textContent = `Level ${Math.min(10, level)}`;
    }

    initSingularitySun() {
        const canvas = document.getElementById("singularity-canvas");
        const ctx = canvas.getContext("2d");

        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const time = Date.now() * 0.001;

            // Schwarzes Loch (Singularität)
            const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 50);
            gradient.addColorStop(0, "#0a0a0a");
            gradient.addColorStop(0.5, "#1a1a2e");
            gradient.addColorStop(1, "#0a0a0a");

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(centerX, centerY, 50, 0, Math.PI * 2);
            ctx.fill();

            // Pulsierende Ringe
            for (let i = 1; i <= 3; i++) {
                const radius = 60 + i * 30;
                const opacity = 0.3 + Math.sin(time * 2 + i) * 0.2;

                ctx.strokeStyle = `rgba(255, 215, 0, ${opacity})`;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
                ctx.stroke();
            }

            // Frequency-ähnliche Balken
            for (let i = 0; i < 32; i++) {
                const angle = (i / 32) * Math.PI * 2;
                const distance = 70;
                const x = centerX + Math.cos(angle) * distance;
                const y = centerY + Math.sin(angle) * distance;

                const height = 20 + Math.sin(time * 3 + i) * 15;

                ctx.fillStyle = `hsl(${i * 11.25 + time * 100}, 100%, 50%)`;
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(angle);
                ctx.fillRect(-2, 0, 4, height);
                ctx.restore();
            }

            requestAnimationFrame(animate);
        };

        animate();
    }

    createGroupChat(roomName) {
        this.currentRoom = roomName;
        this.chatMessages.innerHTML = "";
        this.messages = [];

        companion.speak(`Willkommen im Chat-Raum: ${roomName}! 🎉`);
    }

    getMessagesInRoom() {
        return this.messages.filter(m => m.room === this.currentRoom);
    }
}

// Initialisiere Chat-System
const chat = new ChatSystem();

