extends Node

var game_started: bool = false
var start_time: float = 0.0

func _ready():
	add_to_group("game_manager")
	_initialize_subsystems()
	start_time = Time.get_ticks_msec()

func _process(delta):
	if not game_started and Time.get_ticks_msec() - start_time > 3000:
		game_started = true
		_show_welcome_complete()

	if Input.is_action_just_pressed("ui_cancel"):
		_toggle_menu()

	# Player movement
	var player = get_node("Player")
	if player:
		var speed = 200.0
		var move = Vector2(
			Input.get_axis("move_left", "move_right"),
			Input.get_axis("move_up", "move_down")
		)
		if move.length() > 0:
			move = move.normalized() * speed * delta
			player.position += move

func _initialize_subsystems():
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

	# Make Tortuga visible after 2 seconds
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

func get_persistence():
	return get_node_or_null("Persistence")
