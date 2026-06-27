extends Node2D

signal completed(score: float, details: Dictionary)

enum Rule { SHAPE, COLOR }

const SHAPES = ["circle", "square", "triangle"]
const SHAPE_NAMES = ["Círculo", "Cuadrado", "Triángulo"]
const COLORS = ["rojo", "azul", "amarillo"]
const COLOR_VALUES = [
	Color(0.9, 0.15, 0.15),
	Color(0.15, 0.30, 0.95),
	Color(0.95, 0.90, 0.10)
]

var current_rule: int = Rule.SHAPE
var correct_in_rule = 0
var rule_change_at = 5
var total_correct = 0
var total_errors = 0
var current_card_data: Dictionary = {}
var round_active = false
var rule_changes = 0
var max_score_before_change = 0

var rule_label: Label
var score_label: Label
var prompt_label: Label
var feedback_label: Label
var instruction_label: Label
var card_container: Node2D
var target_zones: Array = []
var card_node: Node2D

var screen_size: Vector2

func _ready():
	screen_size = get_viewport_rect().size
	build_ui()
	build_target_zones()
	await get_tree().create_timer(0.3).timeout
	new_card()

func build_ui():
	var bg = ColorRect.new()
	bg.color = Color(0.10, 0.12, 0.22, 0.97)
	bg.size = screen_size
	bg.position = Vector2.ZERO
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)

	var title = Label.new()
	title.text = "🌊 El Río de Reglas"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 48)
	title.add_theme_color_override("font_color", Color(1, 1, 1))
	title.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.6))
	title.add_theme_constant_override("shadow_offset", 3)
	title.position = Vector2(0, 20)
	title.size = Vector2(screen_size.x, 60)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	instruction_label = Label.new()
	instruction_label.text = "Clasificá cada carta en el grupo correcto.\nLa regla cambia sin aviso, ¡prestá atención!"
	instruction_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	instruction_label.add_theme_font_size_override("font_size", 20)
	instruction_label.add_theme_color_override("font_color", Color(0.75, 0.80, 1.0))
	instruction_label.position = Vector2(100, 72)
	instruction_label.size = Vector2(screen_size.x - 200, 50)
	instruction_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(instruction_label)

	rule_label = Label.new()
	rule_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	rule_label.add_theme_font_size_override("font_size", 24)
	rule_label.add_theme_color_override("font_color", Color(0.6, 0.9, 1.0))
	rule_label.position = Vector2(0, 124)
	rule_label.size = Vector2(screen_size.x, 36)
	rule_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(rule_label)

	prompt_label = Label.new()
	prompt_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt_label.add_theme_font_size_override("font_size", 22)
	prompt_label.add_theme_color_override("font_color", Color(0.9, 0.9, 0.6))
	prompt_label.position = Vector2(0, 158)
	prompt_label.size = Vector2(screen_size.x, 30)
	prompt_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(prompt_label)

	score_label = Label.new()
	score_label.add_theme_font_size_override("font_size", 26)
	score_label.add_theme_color_override("font_color", Color(1, 1, 0.7))
	score_label.position = Vector2(30, screen_size.y - 50)
	score_label.size = Vector2(400, 36)
	score_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(score_label)

	feedback_label = Label.new()
	feedback_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	feedback_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	feedback_label.add_theme_font_size_override("font_size", 56)
	feedback_label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.8))
	feedback_label.add_theme_constant_override("shadow_offset", 4)
	feedback_label.position = Vector2(screen_size.x / 2 - 200, screen_size.y / 2 - 50)
	feedback_label.size = Vector2(400, 100)
	feedback_label.visible = false
	feedback_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(feedback_label)

	update_rule_display()
	update_score()

func build_target_zones():
	var zone_width = 280
	var zone_height = 240
	var gap = 30
	var total_width = 4 * zone_width + 3 * gap
	var start_x = (screen_size.x - total_width) / 2 + zone_width / 2
	var zone_y = screen_size.y * 0.58

	var zone_labels = []
	if current_rule == Rule.SHAPE:
		zone_labels = SHAPE_NAMES
	else:
		zone_labels = ["Rojo", "Azul", "Amarillo"]

	var zone_colors = [
		Color(0.3, 0.2, 0.4, 0.7),
		Color(0.2, 0.3, 0.4, 0.7),
		Color(0.3, 0.3, 0.2, 0.7),
		Color(0.25, 0.2, 0.35, 0.7)
	]

	for i in range(4):
		var zone = build_target_zone(
			Vector2(start_x + i * (zone_width + gap), zone_y),
			zone_width, zone_height,
			zone_labels[i % zone_labels.size()],
			zone_colors[i],
			i
		)
		target_zones.append(zone)
		add_child(zone)

func build_target_zone(pos: Vector2, w: float, h: float, label_text: String, color: Color, idx: int) -> Node2D:
	var container = Node2D.new()
	container.position = pos

	var bg_rect = ColorRect.new()
	bg_rect.color = color
	bg_rect.size = Vector2(w, h)
	bg_rect.position = Vector2(-w / 2, -h / 2)
	bg_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(bg_rect)

	var border = ColorRect.new()
	border.color = Color(1, 1, 1, 0.15)
	border.size = Vector2(w - 4, h - 4)
	border.position = Vector2(-w / 2 + 2, -h / 2 + 2)
	border.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(border)

	var shape_node = Node2D.new()
	shape_node.position = Vector2(0, -20)
	shape_node.name = "ShapeDisplay"
	container.add_child(shape_node)

	var label = Label.new()
	label.text = label_text
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 24)
	label.add_theme_color_override("font_color", Color(1, 1, 1))
	label.position = Vector2(-w / 2, h / 2 - 40)
	label.size = Vector2(w, 36)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(label)

	var area = Area2D.new()
	var collision = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(w, h)
	collision.shape = shape
	area.add_child(collision)
	area.input_event.connect(_on_zone_input.bind(container, idx))
	area.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	container.add_child(area)

	container.set_meta("idx", idx)
	return container

func build_card() -> Node2D:
	var container = Node2D.new()

	var shape_type = randi() % SHAPES.size()
	var color_idx = randi() % COLORS.size()

	var bg = ColorRect.new()
	bg.color = Color(0.2, 0.2, 0.3, 0.9)
	bg.size = Vector2(160, 200)
	bg.position = Vector2(-80, -100)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(bg)

	var border = ColorRect.new()
	border.color = Color(1, 1, 1, 0.2)
	border.size = Vector2(152, 192)
	border.position = Vector2(-76, -96)
	border.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(border)

	var shape_color = COLOR_VALUES[color_idx]
	match shape_type:
		0:
			var c = ColorRect.new()
			c.color = shape_color
			var tex = make_circle_texture(80, shape_color)
			c.texture = tex
			c.size = Vector2(80, 80)
			c.position = Vector2(-40, -50)
			c.mouse_filter = Control.MOUSE_FILTER_IGNORE
			container.add_child(c)
		1:
			var sq = ColorRect.new()
			sq.color = shape_color
			sq.size = Vector2(70, 70)
			sq.position = Vector2(-35, -45)
			sq.mouse_filter = Control.MOUSE_FILTER_IGNORE
			container.add_child(sq)
		2:
			draw_triangle_in_container(container, shape_color)

	var shape_name = Label.new()
	shape_name.text = SHAPE_NAMES[shape_type]
	shape_name.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	shape_name.add_theme_font_size_override("font_size", 18)
	shape_name.add_theme_color_override("font_color", Color(1, 1, 0.8))
	shape_name.position = Vector2(-60, 40)
	shape_name.size = Vector2(120, 30)
	shape_name.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(shape_name)

	var color_label = Label.new()
	color_label.text = COLORS[color_idx].capitalize()
	color_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	color_label.add_theme_font_size_override("font_size", 16)
	color_label.add_theme_color_override("font_color", Color(0.8, 0.8, 1.0))
	color_label.position = Vector2(-60, 65)
	color_label.size = Vector2(120, 24)
	color_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.add_child(color_label)

	current_card_data = {"shape": shape_type, "color": color_idx}
	return container

func draw_triangle_in_container(container: Node2D, color: Color):
	var points = PackedVector2Array([
		Vector2(0, -55),
		Vector2(-40, 25),
		Vector2(40, 25)
	])
	var tri = Polygon2D.new()
	tri.polygon = points
	tri.color = color
	container.add_child(tri)

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

func new_card():
	if card_node:
		card_node.queue_free()

	card_node = build_card()
	var card_pos = Vector2(screen_size.x / 2, screen_size.y * 0.28)
	card_node.position = card_pos + Vector2(screen_size.x, 0)
	add_child(card_node)

	var tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween.tween_property(card_node, "position", card_pos, 0.5)

	round_active = true
	update_rule_display()
	update_prompt()

func _on_zone_input(_viewport: Node, event: InputEvent, _shape_idx: int, container: Node2D, zone_idx: int):
	if not round_active:
		return
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		round_active = false
		var correct = check_match(zone_idx)
		if correct:
			total_correct += 1
			correct_in_rule += 1
			show_feedback(true, "✓ ¡Correcto!")

			if correct_in_rule >= rule_change_at:
				await get_tree().create_timer(0.5).timeout
				change_rule()
			else:
				await get_tree().create_timer(0.3).timeout
				fly_card_to_zone(container)
				await get_tree().create_timer(0.4).timeout
				new_card()
		else:
			total_errors += 1
			show_feedback(false, "✗ Incorrecto")
			shake_card()
			await get_tree().create_timer(0.5).timeout
			round_active = true

func check_match(zone_idx: int) -> bool:
	if current_rule == Rule.SHAPE:
		var expected = current_card_data["shape"]
		return zone_idx == expected
	else:
		var expected = current_card_data["color"]
		return zone_idx == expected

func change_rule():
	rule_changes += 1
	if total_correct > max_score_before_change:
		max_score_before_change = total_correct

	if current_rule == Rule.SHAPE:
		current_rule = Rule.COLOR
	else:
		current_rule = Rule.SHAPE

	correct_in_rule = 0
	update_rule_display()
	update_score()

	for tz in target_zones:
		tz.queue_free()
	target_zones.clear()
	build_target_zones()

	var flash = ColorRect.new()
	flash.color = Color(1, 1, 1, 0.3)
	flash.size = screen_size
	flash.position = Vector2.ZERO
	flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(flash)
	var tween = create_tween()
	tween.tween_property(flash, "modulate", Color(1, 1, 1, 0), 0.5)
	tween.tween_callback(flash.queue_free)

	new_card()

func fly_card_to_zone(zone: Node2D):
	if not card_node:
		return
	var tween = create_tween().set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUINT)
	tween.tween_property(card_node, "position", zone.position + Vector2(0, 30), 0.3)
	tween.tween_property(card_node, "scale", Vector2(0.3, 0.3), 0.2)

func shake_card():
	if not card_node:
		return
	var orig = card_node.position
	var tween = create_tween().set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
	tween.tween_property(card_node, "position", orig + Vector2(10, 0), 0.05)
	tween.tween_property(card_node, "position", orig - Vector2(10, 0), 0.05)
	tween.tween_property(card_node, "position", orig + Vector2(5, 0), 0.05)
	tween.tween_property(card_node, "position", orig, 0.05)

func show_feedback(success: bool, text: String):
	feedback_label.text = text
	feedback_label.add_theme_color_override("font_color", \
		Color(0.3, 1.0, 0.3) if success else Color(1.0, 0.3, 0.3))
	feedback_label.visible = true

	var tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween.tween_property(feedback_label, "scale", Vector2.ONE, 0.3).from(Vector2(2.5, 2.5))
	tween.tween_interval(0.6)
	tween.tween_callback(func():
		feedback_label.visible = false
		feedback_label.scale = Vector2.ONE
	)

func update_rule_display():
	var rule_name = "FORMA" if current_rule == Rule.SHAPE else "COLOR"
	rule_label.text = "Regla actual: clasificar por %s" % rule_name
	rule_label.add_theme_color_override("font_color", \
		Color(0.6, 1.0, 0.6) if current_rule == Rule.SHAPE else Color(1.0, 0.8, 0.4))

func update_prompt():
	if current_card_data.is_empty():
		return
	var shape_name = SHAPE_NAMES[current_card_data["shape"]]
	var color_name = COLORS[current_card_data["color"]].capitalize()
	prompt_label.text = "%s %s — ¿Dónde va?" % [color_name, shape_name]

func update_score():
	score_label.text = "Aciertos: %d  |  Errores: %d  |  Reglas: %d" % [total_correct, total_errors, rule_changes]

func end_game():
	round_active = false

	for child in get_children():
		child.queue_free()

	var final_bg = ColorRect.new()
	final_bg.color = Color(0.10, 0.12, 0.22, 0.95)
	final_bg.size = screen_size
	final_bg.position = Vector2.ZERO
	final_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(final_bg)

	var title = Label.new()
	title.text = "🌊 ¡Completaste el Río de Reglas!"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 42)
	title.add_theme_color_override("font_color", Color(1, 1, 1))
	title.position = Vector2(0, screen_size.y * 0.2)
	title.size = Vector2(screen_size.x, 60)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	var stats = Label.new()
	stats.text = "Aciertos: %d\nErrores: %d\nCambios de regla: %d" % [total_correct, total_errors, rule_changes]
	stats.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stats.add_theme_font_size_override("font_size", 30)
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
	var score_value = float(total_correct) / max(1, total_correct + total_errors) * 10.0
	completed.emit(score_value, {
		"hits": total_correct,
		"errors": total_errors,
		"rule_changes": rule_changes,
		"max_before_change": max_score_before_change,
		"type": "wcst"
	})
	queue_free()
