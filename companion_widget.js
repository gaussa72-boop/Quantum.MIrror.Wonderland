// companion_widget.js - Master-Kater als KI-Begleiter

class CompanionWidget {
    constructor() {
        this.catElement = document.getElementById("cat-speech");
        this.tones = ["mystisch", "chaotisch", "weise", "verrückt"];
        this.currentTone = "mystisch";
        this.personality = {
            mystisch: [
                "Im Nebel der Spiegel erkenne ich:",
                "Die Quantenwelt flüstert:",
                "Zwischen den Welten:",
                "Die Singularität zeigt mir:"
            ],
            chaotisch: [
                "Hahahaha! Chaos bricht aus!",
                "Die Spiegel zerbrechen!",
                "Verrücktheit ist Methode!",
                "Alles tanzt im Quantenfluss!"
            ],
            weise: [
                "Weise Worte:",
                "In meinem Alter weiß ich:",
                "Die Lehre besagt:",
                "Aus den Spiegeln kam die Erkenntnis:"
            ],
            verrückt: [
                "Ganz verrückt, aber wahr:",
                "In der Wahnsinnswelt:",
                "Die Magie sagt:",
                "Im Reich des Unmöglichen:"
            ]
        };
    }

    speak(message, tone = null) {
        tone = tone || this.currentTone;
        const prefix = this.personality[tone][Math.floor(Math.random() * this.personality[tone].length)];
        const fullMessage = `${prefix} ${message}`;

        this.catElement.innerHTML = fullMessage;
        this.animateSpeak();

        return fullMessage;
    }

    animateSpeak() {
        this.catElement.style.animation = "none";
        setTimeout(() => {
            this.catElement.style.animation = "speech-fade 4s ease-in-out infinite";
        }, 10);
    }

    respondToUserInput(userInput, avatarName) {
        // Analysiere User-Input und antworte entsprechend
        let response = "";

        if (userInput.includes("spiel") || userInput.includes("game")) {
            response = `${avatarName}, der möchte ein neues Spiel! Lass mich etwas Magisches für dich kreieren...`;
            this.changeTone("chaotisch");
        } else if (userInput.includes("hilf") || userInput.includes("hilfe")) {
            response = `Aber natürlich helfe ich! Das ist mein Zweck im Quantum Mirror Wonderland!`;
            this.changeTone("weise");
        } else if (userInput.includes("spiegel") || userInput.includes("zerbrechen")) {
            response = `Oh ja! Lass mich einen Spiegel für dich zerbrechen und eine neue Welt erschaffen!`;
            this.changeTone("verrückt");
        } else {
            response = `${avatarName} sagt also: "${userInput}". Faszinierend! Lass mich das verarbeiten...`;
        }

        this.speak(response);
        return response;
    }

    changeTone(newTone) {
        if (this.personality[newTone]) {
            this.currentTone = newTone;
        }
    }

    commentOnAction(action) {
        const comments = {
            "mirror_opened": "Ein Spiegel wird geöffnet! Schau, was sich dahinter verbirgt!",
            "mirror_broken": "KRACH! Die Realität zerbricht! Eine neue Welt entsteht!",
            "game_created": "Voilà! Ein neues Spieluniversum wurde erzeugt!",
            "chat_started": "Das Quantum Geplauder beginnt! Lass uns die Grenzen erkunden!",
            "avatar_evolved": "Dein Avatar wächst! Du wirst mächtiger!"
        };

        const comment = comments[action] || "Etwas Magisches passiert!";
        this.speak(comment);
    }

    reactToEmoji(emoji) {
        const reactions = {
            "🎮": "Oh, ein Spiel! Lass mich kreativ werden!",
            "💎": "Ein Juwel der Weisheit!",
            "🌀": "Die Spirale dreht sich!",
            "✨": "Die Magie wächst!",
            "🪞": "Ein Spiegel! Interessant!"
        };

        const reaction = reactions[emoji] || "Faszinierend!";
        this.speak(reaction);
    }
}

// Initialisiere Companion-Widget
const companion = new CompanionWidget();

// Master-Kater begrüßt User beim Laden
document.addEventListener("DOMContentLoaded", () => {
    companion.speak("Willkommen in der Quantum Mirror Wonderland! Ich bin dein Begleiter. Lass uns Abenteuer erleben!");
});

