extends Node

const MATCH_COUNT =5
const PORTRAIT_DURATION =3.0

@export var portrait_container: Control
@export var quote_label: RichTextLabel
@export var character_scene: PackedScene

var _is_playing =false
var _match_queue: Array = []

func trigger_mirror_scene() -> void:
	if _is_playing:
		return

	var profile = PersonalityEngine.get_profile()
	if profile == null:
		return

	var context = GameManager.current_emotional_state
	var gm = get_node("/root/JardinCentral")
	var matches = gm.get_latent_space().match(gm.get_latent_space().get_profile_3d(), 3)
		profile.to_vector(),
		context,
		MATCH_COUNT
	)

	if matches.is_empty():
		return

	_is_playing = true
	_match_queue = matches.duplicate()
	_play_next_match()

func _play_next_match() -> void:
	if _match_queue.is_empty():
		_is_playing = false
		return

	var match_data = _match_queue.pop_front()

	show_character_portrait(match_data)
	show_quote(match_data.quote)

	await get_tree().create_timer(PORTRAIT_DURATION).timeout
	_play_next_match()

func show_character_portrait(match_data: Dictionary) -> void:
	if portrait_container == null:
		return

	var instance = character_scene.instantiate()
	instance.setup(match_data)

	for child in portrait_container.get_children():
		child.queue_free()

	portrait_container.add_child(instance)

	var tween =create_tween()
	tween.set_ease(Tween.EASE_OUT)
	tween.set_trans(Tween.TRANS_BACK)
	tween.tween_property(instance, "modulate:a", 1.0, 0.5)
	tween.parallel().tween_property(
		instance,
		"scale",
		Vector2.ONE,
		0.5
	)

func show_quote(text: String) -> void:
	if quote_label == nil:
		return

	quote_label.text = text
	quote_label.visible_ratio = 0.0

	var tween =create_tween()
	tween.set_ease(Tween.EASE_OUT)
	tween.set_trans(Tween.TRANS_EXPO)
	tween.tween_property(quote_label, "visible_ratio", 1.0, 1.5)

	var color_tween =create_tween()
	color_tween.tween_property(
		quote_label,
		"modulate:a",
		1.0,
		0.5
	)

func skip() -> void:
	_match_queue.clear()
	_is_playing = false
	hide_all()

func hide_all() -> void:
	if portrait_container:
		for child in portrait_container.get_children():
			child.modulate.a = 0.0
	if quote_label:
		quote_label.modulate.a = 0.0
