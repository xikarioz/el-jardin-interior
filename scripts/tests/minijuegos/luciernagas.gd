extends Node2D

signal completed(score: float, details: Dictionary)

const GRID_COLS = 3
const GRID_ROWS = 3
const FIREFLY_RADIUS = 55.0

var sequence: Array = []
var player_sequence: Array = []
var sequence_length = 2
var max_sequence_length = 0
var lives = 3
var showing_sequence = false
var accepting_input = false
var sequence_index = 0
var game_over = false

var fireflies: Array = []
var lives_label: Label
var score_label: Label
var info_label: Label
var feedback_label: Label
var instruction_label: Label

var screen_size: Vector2

var firefly_colors = [
	Color(1.0, 0.85, 0.3),
	Color(0.3, 1.0, 0.5),
	Color(0.3, 0.7, 1.0),
	Color(1.0, 0.4, 0.7),
	Color(0.8, 0.4, 1.0),
	Color(1.0, 0.6, 0.2),
	Color(0.2, 0.9, 0.9),
	Color(1.0, 1.0, 0.5),
	Color(0.9, 0.5, 0.5)
]

func _ready():
	screen_size = get_viewport_rect().size
	build_ui()
	build_grid()
	await get_tree().create_timer(0.5).timeout
	play_sequence()

func build_ui():
	var bg = ColorRect.new()
	bg.color = Color(0.05, 0.08, 0.15, 0.97)
	bg.size = screen_size
	bg.position = Vector2.ZERO
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)

	var title = Label.new()
	title.text = "✨ Luciérnagas"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 52)
	title.add_theme_color_override("font_color", Color(1, 1, 1))
	title.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.6))
	title.add_theme_constant_override("shadow_offset", 3)
	title.position = Vector2(0, 24)
	title.size = Vector2(screen_size.x, 64)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	instruction_label = Label.new()
	instruction_label.text = "Mirá la secuencia y repetila tocando las luciérnagas en el mismo orden"
	instruction_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	instruction_label.add_theme_font_size_override("font_size", 20)
	instruction_label.add_theme_color_override("font_color", Color(0.75, 0.80, 1.0))
	instruction_label.position = Vector2(100, 80)
	instruction_label.size = Vector2(screen_size.x - 200, 36)
	instruction_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(instruction_label)

	info_label = Label.new()
	info_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info_label.add_theme_font_size_override("font_size", 24)
	info_label.add_theme_color_override("font_color", Color(0.8, 0.9, 1.0))
	info_label.position = Vector2(0, 124)
	info_label.size = Vector2(screen_size.x, 36)
	info_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(info_label)

	lives_label = Label.new()
	lives_label.add_theme_font_size_override("font_size", 28)
	lives_label.add_theme_color_override("font_color", Color(1, 0.4, 0.4))
	lives_label.position = Vector2(30, 30)
	lives_label.size = Vector2(200, 36)
	lives_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(lives_label)

	score_label = Label.new()
	score_label.add_theme_font_size_override("font_size", 28)
	score_label.add_theme_color_override("font_color", Color(1, 1, 0.7))
	score_label.position = Vector2(30, screen_size.y - 60)
	score_label.size = Vector2(400, 36)
	score_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(score_label)

	feedback_label = Label.new()
	feedback_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	feedback_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	feedback_label.add_theme_font_size_override("font_size", 64)
	feedback_label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.8))
	feedback_label.add_theme_constant_override("shadow_offset", 4)
	feedback_label.position = Vector2(screen_size.x / 2 - 200, screen_size.y / 2 - 60)
	feedback_label.size = Vector2(400, 120)
	feedback_label.visible = false
	feedback_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(feedback_label)

	update_ui()

func build_grid():
	var grid_width = GRID_COLS * (FIREFLY_RADIUS * 2 + 30) - 30
	var grid_height = GRID_ROWS * (FIREFLY_RADIUS * 2 + 30) - 30
	var start_x = (screen_size.x - grid_width) / 2 + FIREFLY_RADIUS
	var start_y = (screen_size.y - grid_height) / 2 + FIREFLY_RADIUS - 30

	for row in range(GRID_ROWS):
		for col in range(GRID_COLS):
			var idx = row * GRID_COLS + col
			var pos = Vector2(
				start_x + col * (FIREFLY_RADIUS * 2 + 30),
				start_y + row * (FIREFLY_RADIUS * 2 + 30)
			)
			var ff = build_firefly(pos, idx)
			fireflies.append(ff)
			add_child(ff)

func build_firefly(pos: Vector2, idx: int) -> Node2D:
	var container = Node2D.new()
	container.position = pos

	var glow = TextureRect.new()
	var glow_color = firefly_colors[idx % firefly_colors.size()]
	var glow_tex = make_glow_texture(int(FIREFLY_RADIUS * 2.4), glow_color, 0.3)
	glow.texture = glow_tex
	glow.size = Vector2(FIREFLY_RADIUS * 2.4, FIREFLY_RADIUS * 2.4)
	glow.position = Vector2(-FIREFLY_RADIUS * 1.2, -FIREFLY_RADIUS * 1.2)
	glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glow.visible = false
	glow.name = "Glow"
	container.add_child(glow)

	var body_tex = make_circle_texture(int(FIREFLY_RADIUS * 2), firefly_colors[idx % firefly_colors.size()])
	var body = TextureRect.new()
	body.texture = body_tex
	body.size = Vector2(FIREFLY_RADIUS * 2, FIREFLY_RADIUS * 2)
	body.position = Vector2(-FIREFLY_RADIUS, -FIREFLY_RADIUS)
	body.mouse_filter = Control.MOUSE_FILTER_IGNORE
	body.name = "Body"
	container.add_child(body)

	var wings = TextureRect.new()
	var wing_tex = make_ellipse_texture(20, 35, Color(1, 1, 1, 0.4))
	wings.texture = wing_tex
	wings.size = Vector2(20, 35)
	wings.position = Vector2(-30, -FIREFLY_RADIUS - 10)
	wings.mouse_filter = Control.MOUSE_FILTER_IGNORE
	wings.name = "WingL"
	container.add_child(wings)

	var wing_r = TextureRect.new()
	wing_r.texture = wing_tex
	wing_r.size = Vector2(20, 35)
	wing_r.position = Vector2(10, -FIREFLY_RADIUS - 10)
	wing_r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	wing_r.name = "WingR"
	container.add_child(wing_r)

	var area = Area2D.new()
	var collision = CollisionShape2D.new()
	var shape = CircleShape2D.new()
	shape.radius = FIREFLY_RADIUS
	collision.shape = shape
	area.add_child(collision)
	area.input_event.connect(_on_firefly_input.bind(container, idx))
	area.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	container.add_child(area)

	container.set_meta("idx", idx)
	return container

func make_circle_texture(diameter: int, color: Color) -> ImageTexture:
	var img = Image.create(diameter, diameter, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var center = diameter / 2.0
	var rsq = center * center
	for x in range(diameter):
		for y in range(diameter):
			var dx = x - center
			var dy = y - center
			if dx * dx + dy * dy <= rsq:
				img.set_pixel(x, y, color)
	return ImageTexture.create_from_image(img)

func make_glow_texture(diameter: int, color: Color, alpha: float) -> ImageTexture:
	var img = Image.create(diameter, diameter, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var center = diameter / 2.0
	var rsq = center * center
	for x in range(diameter):
		for y in range(diameter):
			var dx = x - center
			var dy = y - center
			var dist_sq = dx * dx + dy * dy
			if dist_sq <= rsq:
				var a = alpha * (1.0 - dist_sq / rsq)
				img.set_pixel(x, y, Color(color.r, color.g, color.b, a))
	return ImageTexture.create_from_image(img)

func make_ellipse_texture(w: int, h: int, color: Color) -> ImageTexture:
	var img = Image.create(w * 2, h * 2, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var cx = w
	var cy = h
	for x in range(w * 2):
		for y in range(h * 2):
			var dx = (x - cx) / float(w)
			var dy = (y - cy) / float(h)
			if dx * dx + dy * dy <= 1.0:
				img.set_pixel(x, y, color)
	return ImageTexture.create_from_image(img)

func _on_firefly_input(_viewport: Node, event: InputEvent, _shape_idx: int, container: Node2D, idx: int):
	if not accepting_input or game_over:
		return
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		light_firefly(container)
		player_sequence.append(idx)

		var expected = sequence[player_sequence.size() - 1]
		if idx != expected:
			lives -= 1
			update_ui()
			show_feedback(false, "✗ Error")
			return

		if player_sequence.size() == sequence.size():
			accepting_input = false
			if sequence_length > max_sequence_length:
				max_sequence_length = sequence_length
			sequence_length = min(sequence_length + 1, 9)
			update_ui()
			show_feedback(true, "✓ ¡Bien!")
			await get_tree().create_timer(0.6).timeout
			next_round()

func light_firefly(container: Node2D, duration: float = 0.3):
	var glow = container.get_node("Glow")
	var body = container.get_node("Body")
	if glow:
		glow.visible = true
	if body:
		body.scale = Vector2(1.3, 1.3)

	var tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BOUNCE)
	tween.tween_interval(duration)
	tween.tween_callback(func():
		if glow:
			glow.visible = false
		if body:
			body.scale = Vector2(1.0, 1.0)
	)

func play_sequence():
	showing_sequence = true
	accepting_input = false
	info_label.text = "Observá la secuencia..."
	info_label.modulate = Color(1, 1, 0.7)

	sequence.clear()
	var available = range(9)
	available.shuffle()
	for i in range(sequence_length):
		sequence.append(available[i])

	await get_tree().create_timer(0.5).timeout

	for idx in sequence:
		var ff = fireflies[idx]
		light_firefly(ff, 0.4)
		await get_tree().create_timer(0.5).timeout

	await get_tree().create_timer(0.3).timeout
	player_sequence.clear()
	accepting_input = true
	showing_sequence = false
	info_label.text = "Ahora repetila tocando las luciérnagas..."
	info_label.modulate = Color(0.7, 1.0, 0.7)

func show_feedback(success: bool, text: String):
	feedback_label.text = text
	feedback_label.add_theme_color_override("font_color", \
		Color(0.3, 1.0, 0.3) if success else Color(1.0, 0.3, 0.3))
	feedback_label.visible = true

	var tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween.tween_property(feedback_label, "scale", Vector2.ONE, 0.3).from(Vector2(2.5, 2.5))
	tween.tween_interval(0.8)
	tween.tween_callback(func():
		feedback_label.visible = false
		feedback_label.scale = Vector2.ONE
		if lives <= 0:
			end_game()
	)

func update_ui():
	var hearts = ""
	for i in range(lives):
		hearts += "❤️"
	hearts += "🖤".repeat(3 - lives)
	lives_label.text = "Vidas: " + hearts
	score_label.text = "Secuencia máxima: %d  |  Actual: %d" % [max_sequence_length, sequence_length]

func next_round():
	player_sequence.clear()
	await get_tree().create_timer(0.3).timeout
	play_sequence()

func end_game():
	game_over = true
	accepting_input = false

	for child in get_children():
		child.queue_free()

	var final_bg = ColorRect.new()
	final_bg.color = Color(0.05, 0.08, 0.15, 0.95)
	final_bg.size = screen_size
	final_bg.position = Vector2.ZERO
	final_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(final_bg)

	var title = Label.new()
	title.text = "✨ ¡Gracias por jugar!"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 44)
	title.add_theme_color_override("font_color", Color(1, 1, 1))
	title.position = Vector2(0, screen_size.y * 0.2)
	title.size = Vector2(screen_size.x, 60)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	var stats = Label.new()
	stats.text = "Secuencia más larga recordada: %d\nNivel alcanzado: %d" % [max_sequence_length, max(1, max_sequence_length - 1)]
	stats.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stats.add_theme_font_size_override("font_size", 32)
	stats.add_theme_color_override("font_color", Color(0.8, 1.0, 0.8))
	stats.position = Vector2(0, screen_size.y * 0.35)
	stats.size = Vector2(screen_size.x, 100)
	stats.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(stats)

	var btn = make_button("Volver al Jardín", Color(0.2, 0.6, 0.3))
	btn.position = Vector2(screen_size.x / 2 - 150, screen_size.y * 0.6)
	btn.size = Vector2(300, 70)
	btn.pressed.connect(_exit_minigame)
	add_child(btn)

func make_button(text: String, color: Color) -> Button:
	var btn = Button.new()
	btn.text = text
	btn.add_theme_font_size_override("font_size", 28)
	var normal = StyleBoxFlat.new()
	normal.bg_color = color
	normal.corner_radius_top_left = 12
	normal.corner_radius_top_right = 12
	normal.corner_radius_bottom_left = 12
	normal.corner_radius_bottom_right = 12
	btn.add_theme_stylebox_override("normal", normal)
	var hover = normal.duplicate()
	hover.bg_color = color.lightened(0.2)
	btn.add_theme_stylebox_override("hover", hover)
	return btn

func _exit_minigame():
	var score_value = float(max_sequence_length)
	completed.emit(score_value, {
		"max_sequence": max_sequence_length,
		"lives_remaining": lives,
		"type": "corsi"
	})
	queue_free()
