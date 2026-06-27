extends Node2D

var profile = null
var current_zone: String = "jardin-central"
var test_active: bool = false

func _ready():
	add_to_group("game_manager")
	_ready_profile()
	_setup_trees()
	_setup_flores()

func _ready_profile():
	var PlayerProfile = load("res://scripts/personality/PlayerProfile.gd")
	if PlayerProfile:
		profile = PlayerProfile.new()

func _setup_trees():
	for i in range(6):
		var trunk = ColorRect.new()
		trunk.size = Vector2(6, 40 + randi() % 30)
		trunk.color = Color(0.4, 0.25, 0.1, 1)
		trunk.position = Vector2(100 + randi() % 1200, 340 - trunk.size.y)
		add_child(trunk)
		
		var foliage = ColorRect.new()
		foliage.size = Vector2(50 + randi() % 30, 40 + randi() % 20)
		foliage.color = Color(0.25 + randf()*0.15, 0.45 + randf()*0.2, 0.15, 0.9)
		foliage.position = trunk.position + Vector2(-22, -35)
		add_child(foliage)

func _setup_flores():
	for i in range(4):
		var f = ColorRect.new()
		var col = [Color(1,0.7,0.7,1), Color(1,0.9,0.6,1), Color(0.7,0.7,1,1), Color(1,0.8,0.5,1)][i]
		f.size = Vector2(12, 12)
		f.color = col
		f.position = Vector2(200 + randi() % 900, 390 + randi() % 80)
		add_child(f)

func _process(delta):
	if test_active: return
	
	var player = get_node("Player")
	if player:
		var speed = 180.0
		var move = Vector2(
			Input.get_axis("ui_left", "ui_right"),
			Input.get_axis("ui_up", "ui_down")
		)
		if move.length() > 0:
			move = move.normalized() * speed * delta
			player.position += move
			player.position.x = clamp(player.position.x, 30, 1870)
			player.position.y = clamp(player.position.y, 230, 700)

	var zones = get_tree().get_nodes_in_group("test_zone")
	for z in zones:
		if z.has_method("has_overlapping_bodies"):
			for body in z.get_overlapping_bodies():
				if body == player:
					launch_minigame(z.get_meta("test_type", ""), z.get_meta("biome", ""))

func launch_minigame(test_type: String, biome: String):
	if test_active or test_type == "": return
	test_active = true
	
	var path = "res://scenes/tests/%s.tscn" % test_type
	if ResourceLoader.exists(path):
		var scene = load(path).instantiate()
		add_child(scene)
		if scene.has_signal("completed"):
			scene.completed.connect(_on_minigame_completed.bind(test_type))
	else:
		var label = Label.new()
		label.text = "🔧 Minijuego %s en construcción..." % test_type
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.add_theme_font_size_override("font_size", 24)
		label.position = Vector2(200, 200)
		label.size = Vector2(900, 300)
		add_child(label)
		await get_tree().create_timer(2.0).timeout
		label.queue_free()
		test_active = false

func _on_minigame_completed(score: float, details: Dictionary, test_type: String):
	var bubble = get_node_or_null("CanvasLayer/DialogBubble")
	if bubble:
		bubble.text = "✅ %s completado! Score: %.0f/100" % [test_type, score]
		await get_tree().create_timer(3.0).timeout
		bubble.text = "🌿 Seguí explorando..."
	
	if profile and profile.has_method("adjust"):
		profile.adjust("atencion", score * 0.1)
	
	test_active = false
