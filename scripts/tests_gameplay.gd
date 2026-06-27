extends Node

signal test_completed(biome: String, score: float)
signal test_failed(biome: String, reason: String)

@export var minigame_container: Control
@export var loading_label: Label

var _active_test: Dictionary = {}
var _current_minigame: Node = null

func start_biome_test(biome: String) -> void:
	if _current_minigame != null:
		return

	var gm = get_node("/root/JardinCentral")
	var test = gm.get_test_engine().get_test_for_biome(
		biome, 0
	)

	if test == null:
		test_failed.emit(biome, "no_test_available")
		return

	_active_test = test.duplicate()
	_show_loading(biome)

	var scene_path = "res://scenes/tests/%s.tscn" % test.mechanic_type
	var minigame_resource =ResourceLoader.load_threaded_request(
		scene_path,
		"PackedScene",
		true
	)

	if minigame_resource == null:
		test_failed.emit(biome, "invalid_mechanic_type")
		_active_test = {}
		return

	await _wait_for_load(scene_path)
	_instantiate_minigame(scene_path, test)

func _show_loading(biome: String) -> void:
	if loading_label:
		loading_label.text = "Preparando prueba para %s..." % biome

func _wait_for_load(scene_path: String):
	var progress = []
	while true:
		var status = ResourceLoader.load_threaded_get_status(
			scene_path, progress
		)
		if status == ResourceLoader.THREAD_LOAD_LOADED:
			return
		if status == ResourceLoader.THREAD_LOAD_FAILED:
			push_error("Error cargando escena: ", scene_path)
			return
		await get_tree().process_frame

func _instantiate_minigame(scene_path: String, test: Dictionary) -> void:
	var packed = ResourceLoader.load_threaded_get(scene_path) as PackedScene
	if packed == null:
		test_failed.emit(test.get("biome", "unknown"), "load_failed")
		_active_test = {}
		return

	_clear_minigame()

	_current_minigame = packed.instantiate()
	minigame_container.add_child(_current_minigame)

	if _current_minigame.has_signal("completed"):
		_current_minigame.completed.connect(
			_on_test_completed.bind(_active_test)
		)
	else:
		_current_minigame.connect("game_finished", _on_minigame_finished)

	if _current_minigame.has_method("configure"):
		_current_minigame.configure(test)

	if loading_label:
		loading_label.hide()

func _on_test_completed(score, test) -> void:
	var biome = test.get("biome", "unknown")
	var gm = get_node("/root/JardinCentral")
	if gm and gm.get_test_engine():
		gm.get_test_engine().register_result(biome, score)
	test_completed.emit(biome, score)
	_active_test.clear()

	var tween = create_tween()
	tween.set_ease(Tween.EASE_OUT)
	tween.set_trans(Tween.TRANS_ELASTIC)
	tween.tween_callback(_clear_minigame)
	tween.tween_interval(0.5)

func _on_minigame_finished(result: Dictionary) -> void:
	var score = result.get("score", 0.0)
	_on_test_completed(score, _active_test)

func _clear_minigame() -> void:
	if _current_minigame:
		_current_minigame.queue_free()
		_current_minigame = null

func cancel_active_test() -> void:
	if _current_minigame:
		var biome = _active_test.get("biome", "unknown")
		_clear_minigame()
		_active_test = {}
		test_failed.emit(biome, "cancelled")
