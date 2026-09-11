"""HTTP API for the Dunkle Spiegel / Quantum Game Studio."""
from flask import jsonify, request, send_file
from game_engine import QuantumGameEngine, GameGenerationError
from quantum_game_engine.pipeline import GenerationSpec, GenerationPipeline
from quantum_game_engine.rendering import profile_for


def register_studio_routes(app):
    engine = QuantumGameEngine()
    pipeline = GenerationPipeline()

    @app.get('/studio')
    def studio():
        return app.send_static_file('game_studio.html')

    @app.get('/api/generator/health')
    def generator_health():
        import os
        return jsonify({
            'status': 'ready',
            'ai_provider': 'openai' if os.getenv('OPENAI_API_KEY') else 'local-fallback',
            'model': engine.model,
            'targets': ['web', 'godot', 'unity', 'unreal'],
            'artifacts': ['game', 'dlc', 'mod'],
            'quality_presets': ['4k_ultra', '1440p_high', '1080p_balanced'],
        })

    @app.post('/api/generator/plan')
    def generator_plan():
        data = request.get_json(silent=True) or {}
        try:
            spec = GenerationSpec(
                prompt=data.get('prompt', ''), kind=data.get('kind', 'game'),
                target=data.get('target', 'web'), quality=data.get('quality', '4k_ultra'),
                target_fps=int(data.get('target_fps', 120)),
                ray_tracing=bool(data.get('ray_tracing', True)), hdr=bool(data.get('hdr', True)),
                dlss_or_upscaling=bool(data.get('upscaling', True)), assets=bool(data.get('assets', True)),
                tests=bool(data.get('tests', True)),
            )
            plan = pipeline.plan(spec)
            plan['render_profile'] = profile_for(spec.target, spec.quality)
            return jsonify(plan)
        except (ValueError, TypeError) as exc:
            return jsonify({'error': str(exc)}), 400

    @app.post('/api/generator/generate')
    def generate_artifact():
        try:
            data = request.get_json(silent=True) or {}
            result = engine.generate(
                data.get('prompt', ''), data.get('target', 'web'), data.get('kind', 'game'),
            )
            result['quality'] = data.get('quality', '4k_ultra')
            result['target_fps'] = int(data.get('target_fps', 120))
            result['render_profile'] = profile_for(result['target'], result['quality'])
            return jsonify(result), 201
        except GameGenerationError as exc:
            return jsonify({'error': str(exc)}), 400
        except (ValueError, TypeError) as exc:
            return jsonify({'error': str(exc)}), 400
        except Exception:
            app.logger.exception('generation failed')
            return jsonify({'error': 'Generation failed. Check the server logs.'}), 500

    @app.get('/api/generator/download/<project_id>')
    def download_artifact(project_id):
        try:
            path = engine.download_path(project_id)
            return send_file(path, as_attachment=True, download_name=path.name, mimetype='application/zip')
        except GameGenerationError as exc:
            return jsonify({'error': str(exc)}), 404
