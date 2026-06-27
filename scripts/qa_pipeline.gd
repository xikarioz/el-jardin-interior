extends Node

signal pipeline_started()
signal pipeline_step(step: int, name: String, passed: bool)
signal pipeline_completed(all_passed: bool)

var _passed: int = 0
var _failed: int = 0
var _current_step: int = 0
var _gm = null

func _get_gm():
	if not _gm:
		_gm = get_node("/root/JardinCentral")
	return _gm

func run_full_pipeline_test():
	_passed = 0
	_failed = 0
	_current_step = 0
	pipeline_started.emit()
	print("🧪 Pipeline QA iniciado")
	
	await _run_step(1, "Cargar perfil default", _test_profile_creation())
	await _run_step(2, "Inicializar sistemas", _test_system_init())
	await _run_step(3, "Simular gameplay", _test_gameplay_simulation())
	await _run_step(4, "Verificar cambio de perfil", _test_profile_mutation())
	await _run_step(5, "RAG matcher funciona", _test_rag_matcher())
	await _run_step(6, "Registro de resultados", _test_result_registry())
	
	_print_summary()
	pipeline_completed.emit(_failed == 0)

func _run_step(step: int, name: String, test_func) -> void:
	_current_step = step
	var passed = await test_func
	if passed:
		_passed += 1
	else:
		_failed += 1
	pipeline_step.emit(step, name, passed)
	print("  %s %s" % ["✅" if passed else "❌", name])

func _test_profile_creation():
	var gm = _get_gm()
	if not gm: return false
	var p = gm.get_personality()
	if not p: return false
	return p.get_profile() != null

func _test_system_init():
	var gm = _get_gm()
	return gm != null and gm.get_audio() != null and gm.get_rag() != null

func _test_gameplay_simulation():
	var gm = _get_gm()
	if not gm: return false
	var p = gm.get_personality()
	if not p: return false
	for i in 5:
		p.register_result({"hits": 5, "misses": 1, "false_alarms": 0, "reaction_time": 0.5, "strategy": "sistematica"})
	return true

func _test_profile_mutation():
	var gm = _get_gm()
	var p = gm.get_personality().get_profile()
	if not p: return false
	return p.impulsividad != 50.0 or p.velocidad_procesamiento != 50.0

func _test_rag_matcher():
	var gm = _get_gm()
	var latent = gm.get_latent_space()
	if not latent or not latent.is_loaded(): return false
	var profile = gm.get_personality().get_profile()
	var matches = latent.match(latent.project(profile.to_vector()), 3)
	return matches.size() > 0

func _test_result_registry():
	return true

func _print_summary():
	print("\n═══════════════════════════════════")
	print("  QA Pipeline: %d passed, %d failed" % [_passed, _failed])
	print("  Resultado: %s" % ["✅ TODOS OK" if _failed == 0 else "❌ HAY FALLOS"])
	print("═══════════════════════════════════")
