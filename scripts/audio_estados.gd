extends Node

enum EmotionalState {
	INTROSPECCION,
	EXPLORACION,
	LOGRO,
	FRUSTRACION,
	TRANQUILIDAD
}

const FRUSTRATION_THRESHOLD =30
const CREATIVITY_THRESHOLD =70
const SOCIAL_THRESHOLD =70

@export var transition_duration: float = 1.5

var _current_state =EmotionalState.INTROSPECCION
var _state_history: Array[EmotionalState] = []

func _ready() -> void:
	get_node("/root/JardinCentral").get_personality().connect("profile_updated", _on_profile_updated)

func _process(_delta: float) -> void:
	var profile = PersonalityEngine.get_profile()
	if profile == null:
		return

	var new_state =_determine_emotional_state(profile)
	if new_state != _current_state:
		_transition_to_state(new_state)

func _determine_emotional_state(profile):
	if profile.tolerancia_frustracion < FRUSTRATION_THRESHOLD:
		return EmotionalState.FRUSTRACION
	if profile.creatividad > CREATIVITY_THRESHOLD:
		return EmotionalState.EXPLORACION
	if profile.cognicion_social > SOCIAL_THRESHOLD:
		return EmotionalState.LOGRO
	if profile.neuroticism < 40 and profile.agreeableness > 60:
		return EmotionalState.TRANQUILIDAD
	return EmotionalState.INTROSPECCION

func _transition_to_state(new_state) -> void:
	var old_state = _current_state
	_current_state = new_state
	_state_history.append(new_state)

	get_node("/root/JardinCentral").get_audio().set_emotional_state(_state_name(new_state))
	get_node("/root/JardinCentral").get_audio().crossfade_to(
		_state_audio_bus(new_state),
		transition_duration
	)

	emit_signal("emotional_state_changed", old_state, new_state)

func _state_name(state) -> String:
	match state:
		EmotionalState.FRUSTRACION:
			return "frustracion"
		EmotionalState.EXPLORACION:
			return "exploracion"
		EmotionalState.LOGRO:
			return "logro"
		EmotionalState.TRANQUILIDAD:
			return "tranquilidad"
		_:
			return "introspeccion"

func _state_audio_bus(state) -> String:
	match state:
		EmotionalState.FRUSTRACION:
			return "music_frustracion"
		EmotionalState.EXPLORACION:
			return "music_exploracion"
		EmotionalState.LOGRO:
			return "music_logro"
		EmotionalState.TRANQUILIDAD:
			return "music_tranquilidad"
		EmotionalState.INTROSPECCION:
			return "music_introspeccion"

func get_current_state():
	return _current_state

func get_state_history() -> Array[EmotionalState]:
	return _state_history.duplicate()

func _on_profile_updated() -> void:
	var profile = PersonalityEngine.get_profile()
	if profile == null:
		return
	get_node("/root/JardinCentral").get_audio().set_parameter("emotional_intensity", profile.neuroticism * 0.01)
