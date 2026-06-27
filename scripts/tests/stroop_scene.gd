extends Control

signal completed(score: float, details: Dictionary)

const WORDS := ["ROJO", "AZUL", "VERDE", "AMARILLO", "VIOLETA"]
const COLORS := {
	"ROJO": Color(1, 0, 0, 1),
	"AZUL": Color(0, 0.2, 1, 1),
	"VERDE": Color(0, 0.8, 0.2, 1),
	"AMARILLO": Color(1, 0.9, 0, 1),
	"VIOLETA": Color(0.6, 0.2, 0.8, 1),
}

var word_label: Label
var timer_bar: ColorRect
var timer_bg: ColorRect
var score_label: Label
var round_label: Label

var flower_containers: Array[Control] = []
var flower_buttons: Array[ColorRect] = []
var flower_labels: Array[Label] = []

var round := 0
var max_rounds := 10
var score := 0
var time_left := 5.0
var correct_index := -1
var round_active := false

var screen_size: Vector2

func _ready():
	screen_size = get_viewport_rect().size
	size = screen_size
	_build_background()
	_build_ui()
	_new_round()

func _build_background():
	var bg := ColorRect.new()
	bg.size = screen_size
	bg.color = Color(0.08, 0.1, 0.18, 0.97)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)

	var gradient_rect := TextureRect.new()
	gradient_rect.size = screen_size
	gradient_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var gt := GradientTexture2D.new()
	gt.gradient = Gradient.new()
	gt.gradient.colors = [Color(0.2, 0.3, 0.5, 0.4), Color(0, 0, 0, 0)]
	gt.fill_from = Vector2(0, 0)
	gt.fill_to = Vector2(0, 1)
	gradient_rect.texture = gt
	add_child(gradient_rect)

	var overlay := ColorRect.new()
	overlay.size = Vector2(screen_size.x, 4)
	overlay.position = Vector2(0, screen_size.y * 0.82)
	overlay.color = Color(0.3, 0.4, 0.6, 0.15)
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(overlay)

func _build_ui():
	var title := Label.new()
	title.text = "🌸 Flores del Bosque"
	title.add_theme_font_size_override("font_size", 38)
	title.add_theme_color_override("font_color", Color(1, 1, 1))
	title.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.6))
	title.add_theme_constant_override("shadow_offset", 3)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.position = Vector2(0, 20)
	title.size = Vector2(screen_size.x, 50)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	var instruction := Label.new()
	instruction.text = "Tocá la flor cuyo COLOR coincide con la PALABRA escrita"
	instruction.add_theme_font_size_override("font_size", 18)
	instruction.add_theme_color_override("font_color", Color(0.7, 0.75, 0.9))
	instruction.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	instruction.position = Vector2(0, 60)
	instruction.size = Vector2(screen_size.x, 30)
	instruction.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(instruction)

	word_label = Label.new()
	word_label.name = "WordLabel"
	word_label.add_theme_font_size_override("font_size", 72)
	word_label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.7))
	word_label.add_theme_constant_override("shadow_offset", 5)
	word_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	word_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	word_label.position = Vector2(0, 100)
	word_label.size = Vector2(screen_size.x, 80)
	word_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(word_label)

	timer_bg = ColorRect.new()
	timer_bg.name = "TimerBg"
	timer_bg.size = Vector2(420, 24)
	timer_bg.position = Vector2((screen_size.x - 420) / 2, 200)
	timer_bg.color = Color(0, 0, 0, 0.35)
	timer_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(timer_bg)

	timer_bar = ColorRect.new()
	timer_bar.name = "TimerBar"
	timer_bar.size = Vector2(416, 20)
	timer_bar.position = Vector2((screen_size.x - 416) / 2, 202)
	timer_bar.color = Color(0.2, 0.9, 0.3, 1)
	timer_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(timer_bar)

	round_label = Label.new()
	round_label.name = "RoundLabel"
	round_label.add_theme_font_size_override("font_size", 20)
	round_label.add_theme_color_override("font_color", Color(0.75, 0.8, 0.95))
	round_label.position = Vector2(20, 20)
	round_label.size = Vector2(150, 30)
	round_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(round_label)

	score_label = Label.new()
	score_label.name = "ScoreLabel"
	score_label.add_theme_font_size_override("font_size", 22)
	score_label.add_theme_color_override("font_color", Color(1, 0.9, 0.4))
	score_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	score_label.position = Vector2(screen_size.x - 160, 20)
	score_label.size = Vector2(140, 30)
	score_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(score_label)

	var flower_y := screen_size.y * 0.52
	var flower_x_positions := [screen_size.x * 0.2, screen_size.x * 0.5, screen_size.x * 0.8]

	for i in range(3):
		var container := Control.new()
		container.name = "Flower%d" % i
		container.size = Vector2(200, 200)
		container.position = Vector2(flower_x_positions[i] - 100, flower_y - 100)
		container.mouse_filter = Control.MOUSE_FILTER_PASS
		add_child(container)
		flower_containers.append(container)

		var rect := ColorRect.new()
		rect.size = Vector2(200, 200)
		rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
		container.add_child(rect)
		flower_buttons.append(rect)

		var lbl := Label.new()
		lbl.add_theme_font_size_override("font_size", 30)
		lbl.add_theme_color_override("font_color", Color(1, 1, 1))
		lbl.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.6))
		lbl.add_theme_constant_override("shadow_offset", 3)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		lbl.size = Vector2(200, 200)
		lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		container.add_child(lbl)
		flower_labels.append(lbl)

func _new_round():
	if round >= max_rounds:
		_end_game()
		return

	round += 1
	time_left = 5.0
	round_active = true

	round_label.text = "Ronda %d/%d" % [round, max_rounds]
	score_label.text = "🌸 %d/%d" % [score, max_rounds]

	var word := WORDS[randi() % WORDS.size()]
	var wrong := WORDS.duplicate()
	wrong.erase(word)
	wrong.shuffle()

	var order := PackedStringArray([word, wrong[0], wrong[1]])
	order.shuffle()

	for i in range(3):
		var fw := order[i]
		flower_buttons[i].color = COLORS[fw]
		flower_labels[i].text = fw
		correct_index = i if fw == word else correct_index

		var c := flower_containers[i]
		c.modulate = Color(1, 1, 1, 0)
		c.scale = Vector2(0.5, 0.5)
		var t := create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BOUNCE)
		t.tween_property(c, "scale", Vector2.ONE, 0.45).set_delay(i * 0.1)
		t.parallel().tween_property(c, "modulate", Color(1, 1, 1, 1), 0.3).set_delay(i * 0.1)

	var ink_colors := WORDS.duplicate()
	ink_colors.erase(word)
	var display_color := COLORS[ink_colors[randi() % ink_colors.size()]]
	word_label.text = word
	word_label.add_theme_color_override("font_color", display_color)
	word_label.modulate = Color(1, 1, 1, 0)
	word_label.scale = Vector2(1.5, 1.5)
	var wt := create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	wt.tween_property(word_label, "modulate", Color(1, 1, 1, 1), 0.3)
	wt.parallel().tween_property(word_label, "scale", Vector2.ONE, 0.4)

func _process(delta):
	if not round_active:
		return
	time_left -= delta
	var pct := maxf(0.0, time_left / 5.0)
	timer_bar.size.x = 416.0 * pct
	timer_bar.color = Color(1.0 - pct, pct * 0.9, 0.0, 1.0)

	if time_left <= 0.0:
		round_active = false
		_on_wrong()

func _input(event):
	if not round_active or not event is InputEventMouseButton or not event.pressed:
		return
	if event.button_index != MOUSE_BUTTON_LEFT:
		return

	for i in range(3):
		var c := flower_containers[i]
		var rect := Rect2(c.position, c.size)
		if rect.has_point(event.position):
			round_active = false
			if i == correct_index:
				_on_correct()
			else:
				_on_wrong()
			return

func _on_correct():
	score += 1
	score_label.text = "🌸 %d/%d" % [score, max_rounds]

	var c := flower_containers[correct_index]
	var t := create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BOUNCE)
	t.tween_property(c, "scale", Vector2(1.25, 1.25), 0.12)
	t.tween_property(c, "scale", Vector2(1.0, 1.0), 0.35)

	_show_feedback("✓", Color(0.3, 1.0, 0.3))
	await get_tree().create_timer(0.5).timeout
	_new_round()

func _on_wrong():
	score = maxi(0, score - 1)
	score_label.text = "🌸 %d/%d" % [score, max_rounds]

	for i in range(3):
		var c := flower_containers[i]
		var orig := c.position
		var s := create_tween().set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
		s.tween_property(c, "position", orig + Vector2(12, 0), 0.04)
		s.tween_property(c, "position", orig - Vector2(12, 0), 0.04)
		s.tween_property(c, "position", orig + Vector2(6, 0), 0.04)
		s.tween_property(c, "position", orig - Vector2(6, 0), 0.04)
		s.tween_property(c, "position", orig, 0.04)

	_show_feedback("✗", Color(1.0, 0.3, 0.3))
	await get_tree().create_timer(0.7).timeout
	_new_round()

func _show_feedback(text: String, color: Color):
	var fb := Label.new()
	fb.text = text
	fb.add_theme_font_size_override("font_size", 80)
	fb.add_theme_color_override("font_color", color)
	fb.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.8))
	fb.add_theme_constant_override("shadow_offset", 5)
	fb.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	fb.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	fb.position = Vector2(screen_size.x / 2.0 - 150, screen_size.y * 0.36)
	fb.size = Vector2(300, 120)
	fb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fb)

	var t := create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	t.tween_property(fb, "scale", Vector2.ONE, 0.25).from(Vector2(3, 3))
	t.tween_interval(0.5)
	t.tween_property(fb, "modulate", Color(1, 1, 1, 0), 0.35)
	t.tween_callback(fb.queue_free)

func _end_game():
	round_active = false
	for c in get_children():
		c.queue_free()

	var bg := ColorRect.new()
	bg.size = screen_size
	bg.color = Color(0.08, 0.1, 0.18, 0.95)
	add_child(bg)

	var fade := TextureRect.new()
	fade.size = screen_size
	fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var gt := GradientTexture2D.new()
	gt.gradient = Gradient.new()
	gt.gradient.colors = [Color(0.2, 0.3, 0.5, 0.25), Color(0, 0, 0, 0)]
	gt.fill_from = Vector2(0, 0)
	gt.fill_to = Vector2(0, 1)
	fade.texture = gt
	add_child(fade)

	var title := Label.new()
	title.text = "🌸 ¡Completaste las Flores del Bosque!"
	title.add_theme_font_size_override("font_size", 36)
	title.add_theme_color_override("font_color", Color(1, 1, 1))
	title.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.6))
	title.add_theme_constant_override("shadow_offset", 3)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.position = Vector2(0, screen_size.y * 0.22)
	title.size = Vector2(screen_size.x, 60)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)

	var pct := float(score) / float(max_rounds) * 100.0
	var rank := "🌱 Semilla"
	if pct >= 70.0:
		rank = "🌸 Flor"
	if pct >= 90.0:
		rank = "🌳 Árbol"

	var stats := Label.new()
	stats.text = "Puntaje: %d / %d\n(%.0f%%) — %s" % [score, max_rounds, pct, rank]
	stats.add_theme_font_size_override("font_size", 30)
	stats.add_theme_color_override("font_color", Color(0.8, 1.0, 0.8))
	stats.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stats.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	stats.position = Vector2(0, screen_size.y * 0.34)
	stats.size = Vector2(screen_size.x, 100)
	stats.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(stats)

	var btn := Button.new()
	btn.text = "Volver al Jardín"
	btn.add_theme_font_size_override("font_size", 28)
	btn.add_theme_color_override("font_color", Color(1, 1, 1))
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.18, 0.6, 0.28)
	normal.border_color = Color(0.3, 0.7, 0.4)
	normal.border_width = 2
	normal.corner_radius_top_left = 14
	normal.corner_radius_top_right = 14
	normal.corner_radius_bottom_left = 14
	normal.corner_radius_bottom_right = 14
	btn.add_theme_stylebox_override("normal", normal)
	var hov := normal.duplicate()
	hov.bg_color = Color(0.25, 0.7, 0.35)
	hov.border_color = Color(0.4, 0.85, 0.5)
	btn.add_theme_stylebox_override("hover", hov)
	btn.position = Vector2(screen_size.x / 2.0 - 140, screen_size.y * 0.58)
	btn.size = Vector2(280, 60)
	btn.pressed.connect(_exit)
	add_child(btn)

	var tween := create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween.tween_property(btn, "scale", Vector2.ONE, 0.4).from(Vector2(0.8, 0.8))

func _exit():
	completed.emit(float(score) / float(max_rounds) * 100.0, {
		"score": score,
		"max": max_rounds,
		"type": "stroop"
	})
	queue_free()
