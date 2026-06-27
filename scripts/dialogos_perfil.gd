extends Node

signal trait_changed(trait_name: String, new_value: float, delta: float)
signal significant_response(animal_id: String, delta: float)

const SIGNIFICANT_DELTA_THRESHOLD =5.0

@export var flower_effect_scene: PackedScene
@export var particle_container: Node

func on_question_answered(animal_id: String, answer: Dictionary) -> void:
	if not _validate_answer(answer):
		push_warning("Respuesta invalida para ", animal_id)
		return

	var trait_name =answer.get("trait_afectado", "") as String
	var delta =answer.get("delta", 0.0) as float

	if trait_name.is_empty():
		push_warning("Respuesta sin trait_afectado")
		return

	get_node("/root/JardinCentral").get_personality().adjust_trait(trait_name, delta)

	trait_changed.emit(trait_name, delta, delta)

	if abs(delta) >= SIGNIFICANT_DELTA_THRESHOLD:
		_on_significant_response(animal_id, delta)

func _validate_answer(answer: Dictionary) -> bool:
	if not answer.has("texto"):
		return false
	if not answer.has("trait_afectado"):
		return false
	if not answer.has("delta"):
		return false
	if typeof(answer.delta) != TYPE_FLOAT and typeof(answer.delta) != TYPE_INT:
		return false
	return true

func _on_significant_response(animal_id: String, delta: float) -> void:
	significant_response.emit(animal_id, delta)

	WorldState.spawn_glowing_flowers(animal_id)

	if particle_container:
		_spawn_flower_particles(delta)

	if delta > 0:
		get_node("/root/JardinCentral").get_audio().play_positive_feedback()
	else:
		get_node("/root/JardinCentral").get_audio().play_negative_feedback()

func _spawn_flower_particles(delta: float) -> void:
	if flower_effect_scene == null:
		return

	var instance = flower_effect_scene.instantiate()
	particle_container.add_child(instance)

	var intensity = clampf(abs(delta) / 20.0, 0.3, 1.0)

	if instance.has_method("set_intensity"):
		instance.set_intensity(intensity)

	if instance.has_method("set_color"):
		var color =_delta_to_color(delta)
		instance.set_color(color)

	var tween =create_tween()
	tween.set_ease(Tween.EASE_OUT)
	tween.set_trans(Tween.TRANS_ELASTIC)
	tween.tween_property(instance, "scale", Vector2.ONE * intensity, 0.5)
	tween.tween_interval(2.0)
	tween.tween_property(instance, "modulate:a", 0.0, 1.0)
	tween.tween_callback(instance.queue_free)

func _delta_to_color(delta: float) -> Color:
	if delta > 0:
		return Color(0.2, 0.9, 0.4, 1.0)
	return Color(0.9, 0.3, 0.3, 1.0)

func get_available_traits() -> Array[String]:
	return PersonalityEngine.get_trait_list()
