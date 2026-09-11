"""HTTP API for the Quantum Game Studio."""
from flask import jsonify, request, send_file
from game_engine import QuantumGameEngine, GameGenerationError

def register_studio_routes(app):
    engine = QuantumGameEngine()
    @app.get('/studio')
    def studio():
        return app.send_static_file('game_studio.html')
    @app.get('/api/generator/health')
    def generator_health():
        import os
        return jsonify({'status':'ready','ai_provider':'openai' if os.getenv('OPENAI_API_KEY') else 'local-fallback','model':engine.model})
    @app.post('/api/generator/generate')
    def generate_artifact():
        try:
            data = request.get_json(silent=True) or {}
            result = engine.generate(data.get('prompt',''), data.get('target','web'), data.get('kind','game'))
            return jsonify(result), 201
        except GameGenerationError as exc:
            return jsonify({'error':str(exc)}), 400
        except Exception:
            app.logger.exception('generation failed')
            return jsonify({'error':'Generation failed. Check the server logs.'}), 500
    @app.get('/api/generator/download/<project_id>')
    def download_artifact(project_id):
        try:
            path = engine.download_path(project_id)
            return send_file(path, as_attachment=True, download_name=path.name, mimetype='application/zip')
        except GameGenerationError as exc:
            return jsonify({'error':str(exc)}), 404
