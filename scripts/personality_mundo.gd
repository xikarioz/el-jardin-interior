extends Node

@export var tilemap: TileMap
@export var flower_spawner: Node
@export var world_environment: WorldEnvironment

var _time_accum: float = 0.0

func _ready() -> void:
	get_node("/root/JardinCentral").get_personality().connect("profile_updated", _on_profile_updated)

func _process(delta: float) -> void:
	var profile = PersonalityEngine.get_profile()
	if profile == null:
		return

	_adjust_tile_colors(profile)
	_adjust_flower_density(profile)
	_adjust_time_of_day(profile, delta)

func _on_profile_updated() -> void:
	var profile = PersonalityEngine.get_profile()
	if profile == null:
		return

	var transition_tween =create_tween()
	transition_tween.set_ease(Tween.EASE_OUT)
	transition_tween.set_trans(Tween.TRANS_CUBIC)

	var target_hue = profile.agreeableness * 0.1 - 0.05
	transition_tween.tween_method(
		_set_hue_shift,
		_get_current_hue(),
		target_hue,
		2.0
	)

func _adjust_tile_colors(profile) -> void:
	if tilemap == null:
		return

	var hue_shift = profile.agreeableness * 0.1 - 0.05
	var saturation = clampf(1.0 - (profile.neuroticism * 0.005), 0.4, 1.0)
	var material =tilemap.material as ShaderMaterial
	if material:
		material.set_shader_parameter("hue_shift", hue_shift)
		material.set_shader_parameter("saturation", saturation)

func _adjust_flower_density(profile) -> void:
	if flower_spawner == null:
		return

	var density = profile.conscientiousness * 0.01
	var glow_intensity = clampf(
		profile.openness * 0.008,
		0.0,
		2.0
	)

	flower_spawner.set("spawn_rate_multiplier", density)
	flower_spawner.set("glow_intensity", glow_intensity)

func _adjust_time_of_day(profile, delta: float) -> void:
	if world_environment == null:
		return

	var target_hour = profile.openness * 0.01 * 24.0
	_time_accum += delta
	if _time_accum < 0.5:
		return

	_time_accum = 0.0
	var env =world_environment.environment
	if env:
		var current = env.sun_latitude
		var target = remap(
			target_hour, 0.0, 24.0,
			-0.4, 0.4
		)
		env.sun_latitude = lerpf(current, target, 0.02)

func _get_current_hue() -> float:
	if tilemap == null:
		return 0.0
	var material =tilemap.material as ShaderMaterial
	if material:
		return material.get_shader_parameter("hue_shift") as float
	return 0.0

func _set_hue_shift(value: float) -> void:
	if tilemap == null:
		return
	var material =tilemap.material as ShaderMaterial
	if material:
		material.set_shader_parameter("hue_shift", value)
