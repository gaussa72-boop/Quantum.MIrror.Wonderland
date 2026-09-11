"""HTTP API for the Dunkle Spiegel / Quantum Game Studio."""
import json
from flask import jsonify, request, send_file
from game_engine import QuantumGameEngine, GameGenerationError
from quantum_game_engine.pipeline import GenerationSpec, GenerationPipeline
from quantum_game_engine.rendering import profile_for
from quantum_game_engine.generation_v2 import GenerationOrchestrator
from quantum_game_engine.credits import CreditLedger, public_catalog, verify_webhook


def register_studio_routes(app):
    engine = QuantumGameEngine(); pipeline = GenerationPipeline(); orchestrator = GenerationOrchestrator(); ledger = CreditLedger()

    @app.get('/studio')
    def studio(): return app.send_static_file('game_studio.html')

    @app.get('/credits')
    def credits_page(): return app.send_static_file('credits.html')

    @app.get('/api/generator/health')
    def generator_health():
        import os
        return jsonify({'status':'ready','ai_provider':'openai' if os.getenv('OPENAI_API_KEY') else 'local-fallback','model':engine.model,'targets':['web','godot','unity','unreal'],'artifacts':['game','dlc','mod'],'quality_presets':['4k_ultra','1440p_high','1080p_balanced'],'pipeline_v2':True})

    @app.get('/api/credits/catalog')
    def credits_catalog(): return jsonify({'currency':'EUR','credit_unit':'generation credit','packages':public_catalog(),'providers':['stripe','crypto']})

    @app.get('/api/credits/balance/<user_id>')
    def credits_balance(user_id): return jsonify({'user_id':str(user_id),'credits':ledger.balance(str(user_id))})

    @app.post('/api/credits/checkout')
    def credits_checkout():
        data=request.get_json(silent=True) or {}; user_id=str(data.get('user_id','')).strip()
        if not user_id: return jsonify({'error':'user_id is required'}),400
        try:
            intent=ledger.create_intent(user_id,data.get('package_id',''),data.get('provider','stripe'))
            return jsonify({'payment_intent':intent.id,'user_id':intent.user_id,'package_id':intent.package_id,'provider':intent.provider,'amount_eur_cents':intent.amount_eur_cents,'credits':intent.credits,'status':'pending','integration':'configure provider checkout and webhook before production use'}),201
        except ValueError as exc: return jsonify({'error':str(exc)}),400

    @app.post('/api/credits/webhook/<provider>')
    def credits_webhook(provider):
        import os
        if provider not in {'stripe','crypto'}: return jsonify({'error':'Unsupported provider'}),400
        raw=request.get_data(); signature=request.headers.get('X-Quantum-Signature',''); secret=os.getenv('STRIPE_WEBHOOK_SECRET' if provider=='stripe' else 'CRYPTO_WEBHOOK_SECRET','')
        if not verify_webhook(raw,signature,secret): return jsonify({'error':'Invalid webhook signature'}),401
        try:
            event=json.loads(raw.decode('utf-8')); intent_id=str(event.get('payment_intent','')); event_id=str(event.get('event_id',''))
            if event.get('status') != 'paid': return jsonify({'status':'ignored'}),200
            granted=ledger.confirm(event_id,intent_id,provider); return jsonify({'status':'credited','credits_granted':granted}),200
        except (ValueError,json.JSONDecodeError,UnicodeDecodeError) as exc: return jsonify({'error':str(exc)}),400

    @app.post('/api/generator/plan')
    def generator_plan():
        data=request.get_json(silent=True) or {}
        try:
            spec=GenerationSpec(prompt=data.get('prompt',''),kind=data.get('kind','game'),target=data.get('target','web'),quality=data.get('quality','4k_ultra'),target_fps=int(data.get('target_fps',120)),ray_tracing=bool(data.get('ray_tracing',True)),hdr=bool(data.get('hdr',True)),dlss_or_upscaling=bool(data.get('upscaling',True)),assets=bool(data.get('assets',True)),tests=bool(data.get('tests',True)))
            plan=pipeline.plan(spec); plan['render_profile']=profile_for(spec.target,spec.quality); plan['blueprint']=orchestrator.build_blueprint(spec.prompt,spec.target,spec.kind,spec.quality); return jsonify(plan)
        except (ValueError,TypeError) as exc: return jsonify({'error':str(exc)}),400

    @app.post('/api/generator/blueprint')
    def generator_blueprint():
        data=request.get_json(silent=True) or {}
        try: return jsonify({'pipeline_version':'2.0','stages':orchestrator.stage_order(),'blueprint':orchestrator.build_blueprint(data.get('prompt',''),data.get('target','web'),data.get('kind','game'),data.get('quality','4k_ultra'))})
        except (ValueError,TypeError) as exc: return jsonify({'error':str(exc)}),400

    @app.post('/api/generator/generate')
    def generate_artifact():
        try:
            data=request.get_json(silent=True) or {}; result=engine.generate(data.get('prompt',''),data.get('target','web'),data.get('kind','game')); result['quality']=data.get('quality','4k_ultra'); result['target_fps']=int(data.get('target_fps',120)); result['pipeline_version']='2.0'; result['render_profile']=profile_for(result['target'],result['quality']); result['blueprint']=orchestrator.build_blueprint(data.get('prompt',''),result['target'],result['kind'],result['quality']); return jsonify(result),201
        except GameGenerationError as exc: return jsonify({'error':str(exc)}),400
        except (ValueError,TypeError) as exc: return jsonify({'error':str(exc)}),400
        except Exception: app.logger.exception('generation failed'); return jsonify({'error':'Generation failed. Check the server logs.'}),500

    @app.get('/api/generator/download/<project_id>')
    def download_artifact(project_id):
        try: path=engine.download_path(project_id); return send_file(path,as_attachment=True,download_name=path.name,mimetype='application/zip')
        except GameGenerationError as exc: return jsonify({'error':str(exc)}),404
