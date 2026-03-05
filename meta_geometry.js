// meta_geometry.js - Dynamische Meta-Geometrien im Hintergrund

class MetaGeometry {
    constructor() {
        this.canvas = document.getElementById("meta-geometry-canvas");
        this.ctx = this.canvas.getContext("2d");
        this.particles = [];
        this.geometries = [];

        this.resizeCanvas();
        window.addEventListener("resize", () => this.resizeCanvas());

        this.initGeometries();
        this.animate();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    initGeometries() {
        // Erstelle Heilige Geometrien
        const colors = ["#ffd700", "#00ced1", "#ff1493", "#9370db", "#00ff7f"];

        for (let i = 0; i < 8; i++) {
            this.geometries.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: 30 + Math.random() * 50,
                type: ["circle", "spiral", "mandala"][Math.floor(Math.random() * 3)],
                color: colors[Math.floor(Math.random() * colors.length)],
                rotation: Math.random() * Math.PI * 2,
                speed: Math.random() * 0.01 + 0.001
            });
        }

        // Erstelle Partikel für Mystik-Effekt
        for (let i = 0; i < 100; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 0.5,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }

    drawCircle(x, y, size, color, rotation) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.rotate(rotation);

        this.ctx.strokeStyle = color;
        this.ctx.globalAlpha = 0.2;
        this.ctx.lineWidth = 2;

        for (let i = 0; i < 5; i++) {
            this.ctx.beginPath();
            this.ctx.arc(0, 0, size - i * 5, 0, Math.PI * 2);
            this.ctx.stroke();
        }

        this.ctx.restore();
    }

    drawSpiral(x, y, size, color, rotation) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.rotate(rotation);

        this.ctx.strokeStyle = color;
        this.ctx.globalAlpha = 0.3;
        this.ctx.lineWidth = 1.5;
        this.ctx.beginPath();

        for (let angle = 0; angle < Math.PI * 4; angle += 0.1) {
            const r = angle * size / (Math.PI * 4);
            const px = r * Math.cos(angle);
            const py = r * Math.sin(angle);

            if (angle === 0) {
                this.ctx.moveTo(px, py);
            } else {
                this.ctx.lineTo(px, py);
            }
        }

        this.ctx.stroke();
        this.ctx.restore();
    }

    drawMandala(x, y, size, color, rotation) {
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.rotate(rotation);

        this.ctx.strokeStyle = color;
        this.ctx.globalAlpha = 0.25;
        this.ctx.lineWidth = 1;

        for (let i = 0; i < 12; i++) {
            const angle = (i / 12) * Math.PI * 2;
            this.ctx.beginPath();
            this.ctx.moveTo(0, 0);
            this.ctx.lineTo(
                Math.cos(angle) * size,
                Math.sin(angle) * size
            );
            this.ctx.stroke();
        }

        this.ctx.beginPath();
        this.ctx.arc(0, 0, size / 2, 0, Math.PI * 2);
        this.ctx.stroke();

        this.ctx.restore();
    }

    updateParticles() {
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            // Wrap around edges
            if (p.x < 0) p.x = this.canvas.width;
            if (p.x > this.canvas.width) p.x = 0;
            if (p.y < 0) p.y = this.canvas.height;
            if (p.y > this.canvas.height) p.y = 0;
        });
    }

    drawParticles() {
        this.particles.forEach(p => {
            this.ctx.fillStyle = `rgba(255, 215, 0, ${p.opacity})`;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const time = Date.now() * 0.0001;

        // Zeichne Geometrien
        this.geometries.forEach(g => {
            g.rotation += g.speed;

            if (g.type === "circle") {
                this.drawCircle(g.x, g.y, g.size, g.color, g.rotation);
            } else if (g.type === "spiral") {
                this.drawSpiral(g.x, g.y, g.size, g.color, g.rotation);
            } else if (g.type === "mandala") {
                this.drawMandala(g.x, g.y, g.size, g.color, g.rotation);
            }
        });

        this.updateParticles();
        this.drawParticles();

        requestAnimationFrame(() => this.animate());
    }
}

// Initialisiere Meta-Geometrien
const metaGeometry = new MetaGeometry();

