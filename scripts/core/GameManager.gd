extends Node2D

var game_started: bool = false
var start_time: float = 0.0
var current_minigame: Node = null
var minigame_active: bool = false

signal test_completed(biome: String, score: float, details: Dictionary)

func _ready():
	add_to_group("game_manager")
	_initialize_subsystems()
	start_time = Time.get_ticks_msec()
	_connect_test_zones()

func _process(delta):
	if not game_started and Time.get_ticks_msec() - start_time > 3000:
		game_started = true
		_show_welcome_complete()

	if Input.is_action_just_pressed("ui_cancel"):
		_toggle_menu()

	if minigame_active:
		return

	var player = get_node("Player")
	if player:
		var speed = 200.0
		var move = Vector2(
			Input.get_axis("ui_left", "ui_right"),
			Input.get_axis("ui_up", "ui_down")
		)
		if move.length() > 0:
			move = move.normalized() * speed * delta
			player.position += move

func _connect_test_zones():
	await get_tree().process_frame
	var zones = get_tree().get_nodes_in_group("test_zone")
	for zone in zones:
		if zone.has_signal("body_entered"):
			zone.body_entered.connect(_on_test_zone_entered.bind(zone))
		elif zone.has_signal("area_entered"):
			zone.area_entered.connect(_on_test_zone_entered.bind(zone))

func _on_test_zone_entered(body, zone: Area2D):
	if minigame_active:
		return
	if body.name == "Player" or body.get_parent().name == "Player":
		var test_type = zone.get_meta("test_type", "")
		var biome = zone.get_meta("biome", "jardin-central")
		if test_type != "":
			launch_minigame(test_type, biome)

func launch_minigame(test_type: String, biome: String = "jardin-central"):
	if minigame_active:
		return
	minigame_active = true

	var scene_path = "res://scenes/tests/" + test_type + ".tscn"
	var packed = load(scene_path)
	if not packed:
		minigame_active = false
		return

	var instance = packed.instantiate()
	current_minigame = instance

	if instance.has_signal("completed"):
		instance.completed.connect(_on_minigame_completed.bind(biome))

	var player = get_node("Player")
	if player:
		player.process_mode = Node.PROCESS_MODE_DISABLED
		player.visible = false

	add_child(instance)

	show_message("🧪 Iniciando prueba...", 1.5)

func _on_minigame_completed(score: float, details: Dictionary, biome: String):
	if current_minigame:
		current_minigame.queue_free()
		current_minigame = null

	minigame_active = false

	var player = get_node("Player")
	if player:
		player.process_mode = Node.PROCESS_MODE_INHERIT
		player.visible = true

	on_test_completed({
		"score": score,
		"biome": biome,
		"details": details
	})

	test_completed.emit(biome, score, details)

func on_test_completed(result: Dictionary):
	var score = result.get("score", 0)
	var biome = result.get("biome", "jardin-central")

	var rank = "🌱 Semilla"
	if score >= 7:
		rank = "🌸 Flor"
	if score >= 9:
		rank = "🌳 Árbol"

	show_message("✓ Prueba completada!\nPuntaje: %.1f — %s" % [score, rank], 3.0)

	var te = get_node_or_null("TestEngine")
	if te and te.has_method("report_result"):
		te.report_result(biome + "_test", result)

func show_message(text: String, duration: float = 2.0):
	var layer = get_node_or_null("CanvasLayer")
	if not layer:
		return
	var existing = layer.get_node_or_null("MessageLabel")
	if existing:
		existing.queue_free()

	var label = Label.new()
	label.name = "MessageLabel"
	label.text = text
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 36)
	label.add_theme_color_override("font_color", Color(1, 1, 1))
	label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.7))
	label.add_theme_constant_override("shadow_offset", 3)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size = Vector2(800, 120)
	label.position = Vector2(
		get_viewport_rect().size.x / 2 - 400,
		get_viewport_rect().size.y / 2 - 60
	)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(label)

	label.modulate = Color(1, 1, 1, 0)
	var tween = create_tween()
	tween.tween_property(label, "modulate", Color(1, 1, 1, 1), 0.3)
	tween.tween_interval(duration)
	tween.tween_property(label, "modulate", Color(1, 1, 1, 0), 0.5)
	tween.tween_callback(label.queue_free)

func _initialize_subsystems():
	var prog = load("res://scripts/core/ProgressionManager.gd").new()
	add_child(prog)
	prog.name = "ProgressionManager"

	var dd = load("res://scripts/core/DialogLoader.gd").new()
	add_child(dd)

	var fe = load("res://scripts/personality/feature_extractor.gd").new()
	add_child(fe)

	var pe = load("res://scripts/personality/PersonalityEngine.gd").new()
	add_child(pe)
	pe.initialize()

	var ls = load("res://scripts/personality/latent_space_3d.gd").new()
	add_child(ls)
	ls.initialize()

	var audio = load("res://scripts/audio/AudioDJ.gd").new()
	add_child(audio)
	audio.initialize()

	var rag = load("res://scripts/rag/RAGMatcher.gd").new()
	add_child(rag)

	var pers = load("res://scripts/core/Persistence.gd").new()
	add_child(pers)
	pers.load_game(0)

	var input = load("res://scripts/core/InputManager.gd").new()
	add_child(input)

	var te = load("res://scripts/tests/TestEngine.gd").new()
	add_child(te)

	get_tree().create_timer(2.0).timeout.connect(_show_tortuga)

func _show_tortuga():
	var tortuga = get_node("Tortuga")
	if tortuga:
		tortuga.visible = true

func _show_welcome_complete():
	var bubble = get_node("CanvasLayer/DialogBubble")
	if bubble:
		bubble.text = "🐢 La Tortuga Sabia está aquí.\n¿Exploramos el jardín?"
		await get_tree().create_timer(5.0).timeout
		bubble.visible = false

func _toggle_menu():
	var menu = get_node_or_null("CanvasLayer/MenuPanel")
	if menu:
		menu.visible = not menu.visible
		get_tree().paused = menu.visible
	else:
		var panel = Panel.new()
		panel.name = "MenuPanel"
		panel.size = Vector2(400, 300)
		panel.position = Vector2(200, 100)
		panel.visible = true
		get_node("CanvasLayer").add_child(panel)
		get_tree().paused = true

func get_personality():
	return get_node_or_null("PersonalityEngine")

func get_audio():
	return get_node_or_null("AudioDJ")

func get_rag():
	return get_node_or_null("RAGMatcher")

func get_latent_space():
	return get_node_or_null("LatentSpace3D")

func get_test_engine():
	return get_node_or_null("TestEngine")

func get_dialog_loader():
	return get_node_or_null("DialogLoader")

func get_feature_extractor():
	return get_node_or_null("FeatureExtractor")

func get_input_manager():
	return get_node_or_null("InputManager")

func get_progression():
	return get_node_or_null("ProgressionManager")

func get_persistence():
	return get_node_or_null("Persistence")
