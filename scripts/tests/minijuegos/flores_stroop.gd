extends Node2D

signal completed(score: float, details: Dictionary)

const COLOR_NAMES = ["ROJO", "AZUL", "VERDE", "AMARILLO", "VIOLETA", "NARANJA"]
const COLOR_VALUES = [
	Color(0.95, 0.15, 0.15),
	Color(0.15, 0.30, 0.95),
	Color(0.15, 0.85, 0.15),
	Color(0.95, 0.90, 0.10),
	Color(0.70, 0.15, 0.85),
	Color(0.95, 0.55, 0.10)
]

var round_num = 0
var max_rounds = 10
var hits = 0
var errors = 0
var round_active = false
var remaining_time = 5.0
var feedback_timer = 0.0
var showing_feedback = false
var current_flowers: Array = []

var timer_label: Label
var score_label: Label
var round_label: Label
var feedback_label: Label
var overlay: ColorRect
var instruction_label: Label

var screen_size: Vector2

func _ready():
	screen_size = get_viewport_rect().size
	build_ui()
	start_round()

func build_ui():
	overlay = ColorRect.new()
	overlay.color = Color(0.08, 0.10, 0.18, 0.97)
	overlay.size = screen_size
	overlay.position = Vector2.ZERO
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(overlay)

	var title = Label.new()
	title.text = "🌸 Flores de Atención"
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
	instruction_label.text = "Tocá la flor cuyo COLOR de tinta coincide con la PALABRA escrita"
	instruction_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	instruction_label.add_theme_font_size_override("font_size", 22)
	instruction_label.add_theme_color_override("font_color", Color(0.75, 0.80, 1.0))
	instruction_label.position = Vector2(100, 88)
	instruction_label.size = Vector2(screen_size.x - 200, 36)
	instruction_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(instruction_label)

	round_label = Label.new()
	round_label.add_theme_font_size_override("font_size", 26)
	round_label.add_theme_color_override("font_color", Color(0.7, 0.9, 0.7))
	round_label.position = Vector2(30, 30)
	round_label.size = Vector2(200, 36)
	round_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(round_label)

	timer_label = Label.new()
	timer_label.add_theme_font_size_override("font_size", 40)
	timer_label.add_theme_color_override("font_color", Color(1, 1, 1))
	timer_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	timer_label.position = Vector2(screen_size.x - 160, 24)
	timer_label.size = Vector2(130, 50)
	timer_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(timer_label)

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
	feedback_label.add_theme_font_size_override("font_size", 72)
	feedback_label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.8))
	feedback_label.add_theme_constant_override("shadow_offset", 5)
	feedback_label.position = Vector2(screen_size.x / 2 - 200, screen_size.y / 2 - 60)
	feedback_label.size = Vector2(400, 120)
	feedback_label.visible = false
	feedback_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(feedback_label)

func _process(delta):
	if not round_active or showing_feedback:
		return
	remaining_time -= delta
	timer_label.text = "%.1fs" % remaining_time
	timer_label.add_theme_color_override("font_color", \
		Color(1, 0.5, 0.3) if remaining_time < 2.0 else Color(1, 1, 1))

	if remaining_time <= 0:
		round_active = false
		errors += 1
		show_feedback(false, "¡Se acabó el tiempo!")

func start_round():
	if round_num >= max_rounds:
		end_game()
		return

	round_num += 1
	remaining_time = 5.0
	round_active = true
	showing_feedback = false

	clear_flowers()
	round_label.text = "Ronda %d/%d" % [round_num, max_rounds]
	update_score()

	var correct_color_idx = randi() % COLOR_NAMES.size()
	var correct_word_idx = correct_color_idx
	var wrong_indices = []
	for i in range(COLOR_NAMES.size()):
		if i != correct_color_idx:
			wrong_indices.append(i)
	wrong_indices.shuffle()

	var positions = [
		Vector2(screen_size.x * 0.20, screen_size.y * 0.52),
		Vector2(screen_size.x * 0.50, screen_size.y * 0.52),
		Vector2(screen_size.x * 0.80, screen_size.y * 0.52)
	]

	if round_num > 1 and randi() % 3 == 0:
		positions.shuffle()

	correct_index = randi() % 3

	for i in range(3):
		var is_correct = (i == correct_index)
		var w_idx: int
		var c_idx: int
		if is_correct:
			w_idx = correct_word_idx
			c_idx = correct_color_idx
		else:
			w_idx = wrong_indices[i]
			c_idx = wrong_indices[(i + 1) % wrong_indices.size()]

		var flower = build_flower(positions[i], w_idx, c_idx, is_correct)
		current_flowers.append(flower)
		add_child(flower)

		flower.scale = Vector2.ZERO
		var tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BOUNCE)
		tween.tween_property(flower, "scale", Vector2.ONE, 0.6).set_delay(i * 0.12)

func build_flower(pos: Vector2, word_idx: int, ink_idx: int, correct: bool) -> Node2D:
	var container = Node2D.new()
	container.position = pos

	var circle = TextureRect.new()
	var tex = make_circle_texture(170, COLOR_VALUES[ink_idx])
	circle.texture = tex
	circle.size = Vector2(170, 170)
	circle.position = Vector2(-85, -85)
	circle.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(circle)

	var petal_tex = make_circle_texture(60, COLOR_VALUES[ink_idx].lightened(0.3))
	for p in range(5):
		var petal = TextureRect.new()
		petal.texture = petal_tex
		petal.size = Vector2(60, 60)
		var angle = p * 2.0 * PI / 5.0 - PI / 2.0
		petal.position = Vector2(cos(angle) * 75 - 30, sin(angle) * 75 - 30)
		petal.mouse_filter = Control.MOUSE_FILTER_IGNORE
		container.add_child(petal)

	var label = Label.new()
	label.text = COLOR_NAMES[word_idx]
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 32)
	label.add_theme_color_override("font_color", Color(1, 1, 1))
	label.add_theme_constant_override("shadow_offset", 3)
	label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.7))
	label.size = Vector2(170, 50)
	label.position = Vector2(-85, -25)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(label)

	var area = Area2D.new()
	var collision = CollisionShape2D.new()
	var shape = CircleShape2D.new()
	shape.radius = 85
	collision.shape = shape
	area.add_child(collision)
	area.input_event.connect(_on_flower_input.bind(container, correct))
	area.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	container.add_child(area)

	container.set_meta("correct", correct)
	return container

func make_circle_texture(diameter: float, color: Color) -> ImageTexture:
	var size = int(diameter)
	var img = Image.create(size, size, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var center = size / 2.0
	var radius_sq = (size / 2.0) * (size / 2.0)
	for x in range(size):
		for y in range(size):
			var dx = x - center
			var dy = y - center
			if dx * dx + dy * dy <= radius_sq:
				img.set_pixel(x, y, color)
	return ImageTexture.create_from_image(img)

func _on_flower_input(_viewport: Node, event: InputEvent, _shape_idx: int, container: Node2D, correct: bool):
	if not round_active or showing_feedback:
		return
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		round_active = false
		if correct:
			hits += 1
			show_feedback(true, "✓ ¡Correcto!")
		else:
			errors += 1
			show_feedback(false, "✗ Incorrecto")

func show_feedback(success: bool, text: String):
	showing_feedback = true
	feedback_label.text = text
	feedback_label.add_theme_color_override("font_color", \
		Color(0.3, 1.0, 0.3) if success else Color(1.0, 0.3, 0.3))
	feedback_label.visible = true

	if success:
		highlight_correct_flower()
	else:
		shake_flowers()
		highlight_correct_flower()

	var tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween.tween_property(feedback_label, "scale", Vector2.ONE, 0.3).from(Vector2(3, 3))
	tween.tween_interval(1.2)
	tween.tween_callback(_next_round)

func highlight_correct_flower():
	for f in current_flowers:
		if f.get_meta("correct", false):
			var tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BOUNCE)
			tween.tween_property(f, "scale", Vector2(1.3, 1.3), 0.3)
			tween.tween_property(f, "scale", Vector2(1.0, 1.0), 0.3)

func shake_flowers():
	for f in current_flowers:
		var orig = f.position
		var tween = create_tween().set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
		tween.tween_property(f, "position", orig + Vector2(8, 0), 0.05)
		tween.tween_property(f, "position", orig - Vector2(8, 0), 0.05)
		tween.tween_property(f, "position", orig + Vector2(4, 0), 0.05)
		tween.tween_property(f, "position", orig - Vector2(4, 0), 0.05)
		tween.tween_property(f, "position", orig, 0.05)

func clear_flowers():
	for f in current_flowers:
		f.queue_free()
	current_flowers.clear()

func update_score():
	score_label.text = "✓ %d   ✗ %d   Puntaje: %d" % [hits, errors, hits - errors]

func _next_round():
	feedback_label.visible = false
	feedback_label.scale = Vector2.ONE
	showing_feedback = false
	update_score()
	start_round()

func end_game():
	round_active = false
	clear_flowers()

	for child in get_children():
		if child != overlay and child != timer_label and child != score_label \
			and child != round_label and child != feedback_label and child != instruction_label:
			child.queue_free()

	var final = ColorRect.new()
	final.color = Color(0.08, 0.10, 0.18, 0.9)
	final.size = screen_size
	final.position = Vector2.ZERO
	final.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(final)

	var title = Label.new()
	title.text = "🌸 ¡Completaste las Flores de Atención!"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 40)
	title.add_theme_color_override("font_color", Color(1, 1, 1))
	title.position = Vector2(0, screen_size.y * 0.2)
	title.size = Vector2(screen_size.x, 60)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	var stats = Label.new()
	var final_score = max(0, hits - errors)
	stats.text = "Aciertos: %d\nErrores: %d\nPuntaje final: %d/10" % [hits, errors, final_score]
	stats.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stats.add_theme_font_size_override("font_size", 32)
	stats.add_theme_color_override("font_color", Color(0.8, 1.0, 0.8))
	stats.position = Vector2(0, screen_size.y * 0.35)
	stats.size = Vector2(screen_size.x, 120)
	stats.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(stats)

	var continue_btn = make_button("Volver al Jardín", Color(0.2, 0.6, 0.3))
	continue_btn.position = Vector2(screen_size.x / 2 - 150, screen_size.y * 0.65)
	continue_btn.size = Vector2(300, 70)
	continue_btn.pressed.connect(_exit_minigame.bind(final_score))
	add_child(continue_btn)

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

func _exit_minigame(score: float):
	completed.emit(score, {
		"hits": hits,
		"errors": errors,
		"total_rounds": max_rounds,
		"type": "stroop"
	})
	queue_free()
