extends Node

@export var tile_map: TileMap

const BASE_COLOR =Color(1, 1, 1, 1)

func apply_profile_17(profile) -> void:
	if not tile_map:
		return
	modulate_color(profile_17.neuroticism, profile_17.agreeableness)
	adjust_vegetation(profile_17.conscientiousness)
	adjust_animals(profile_17.extraversion)
	adjust_paths(profile_17.openness)

func apply_latent_3d(pos_3d: Vector3) -> void:
	if not tile_map:
		return
	
	# X: openness/rigidity → curvas vs rectas (hue shift)
	var hue = remap(pos_3d.x, -3.0, 3.0, 0.05, 0.35)
	
	# Y: energy → brightness  
	var brightness = remap(pos_3d.y, -3.0, 3.0, 0.4, 1.0)
	
	# Z: stability → saturation
	var saturation = remap(pos_3d.z, -3.0, 3.0, 0.3, 1.0)
	
	var color = Color.from_hsv(hue, saturation, brightness)
	tile_map.modulate = color
	adjust_brightness(profile_17.agreeableness)
	adjust_water(profile_17.neuroticism)
	adjust_soundscape(profile_17.extraversion, profile_17.neuroticism)

func modulate_color(neuroticism: float, agreeableness: float) -> void:
	var n =clampf(neuroticism, -1.0, 1.0)
	var a =clampf(agreeableness, -1.0, 1.0)

	var warmth =0.5 + a * 0.3
	var desaturation =clampf(0.15 + n * 0.25, 0.0, 0.5)

	var color =BASE_COLOR
	color.r = clampf(BASE_COLOR.r * (warmth + 0.3), 0.4, 1.2)
	color.g = clampf(BASE_COLOR.g * (1.0 - desaturation), 0.3, 1.2)
	color.b = clampf(BASE_COLOR.b * (1.0 - desaturation * 0.5), 0.3, 1.2)

	var layer =tile_map as TileMap
	layer.modulate = color

	if animation_player and animation_player.has_animation("color_transition"):
		animation_player.play("color_transition")

func adjust_vegetation(conscientiousness: float) -> void:
	var c =clampf(conscientiousness, -1.0, 1.0)
	var density =0.3 + (c + 1.0) * 0.35

	for cell in _get_all_tile_cells():
		var tile =tile_map.get_cell_source_id(0, cell)
		if _is_vegetation(tile):
			var keep =randf() < density
			if not keep:
				tile_map.set_cell(0, cell, -1)

func adjust_animals(extraversion: float) -> void:
	var e =clampf(extraversion, -1.0, 1.0)
	var activity_mult =0.4 + (e + 1.0) * 0.4

	for animal in get_tree().get_nodes_in_group("animals"):
		if animal.has_method("set_activity_multiplier"):
			animal.set_activity_multiplier(activity_mult)
		if animal.has_property("animation_speed"):
			animal.animation_speed = 0.6 + e * 0.5

func adjust_paths(openness: float) -> void:
	var o =clampf(openness, -1.0, 1.0)
	var path_complexity =0.3 + (o + 1.0) * 0.35

	if tile_map.has_method("set_path_complexity"):
		tile_map.set_path_complexity(path_complexity)

	var path_layer =tile_map as TileMap
	for cell in _get_all_tile_cells():
		var tile =path_layer.get_cell_source_id(1, cell)
		if _is_path(tile):
			var visible =randf() < path_complexity
			path_layer.set_cell(1, cell, tile if visible else -1)

func adjust_brightness(agreeableness: float) -> void:
	var a =clampf(agreeableness, -1.0, 1.0)
	var brightness =0.5 + a * 0.35
	var layer =tile_map as TileMap
	if layer.has_method("set_brightness"):
		layer.set_brightness(brightness)

	var light =_find_light_node()
	if light:
		light.light_energy = brightness

func adjust_water(neuroticism: float) -> void:
	var n =clampf(neuroticism, -1.0, 1.0)
	var turbulence =0.1 + (n + 1.0) * 0.3

	for water in get_tree().get_nodes_in_group("water"):
		if water.has_method("set_turbulence"):
			water.set_turbulence(turbulence)

func adjust_soundscape(extraversion: float, neuroticism: float) -> void:
	var e =clampf(extraversion, -1.0, 1.0)
	var n =clampf(neuroticism, -1.0, 1.0)

	var volume_db =linear_to_db(0.3 + e * 0.25)
	var pitch_scale =0.9 - n * 0.15

	for audio in get_tree().get_nodes_in_group("ambient_audio"):
		audio.volume_db = volume_db
		audio.pitch_scale = pitch_scale

func _get_all_tile_cells() -> Array:
	var rect =tile_map.get_used_rect()
	var cells: Array = []
	for x in range(rect.position.x, rect.position.x + rect.size.x):
		for y in range(rect.position.y, rect.position.y + rect.size.y):
			cells.append(Vector2i(x, y))
	return cells

func _is_vegetation(tile_id: int) -> bool:
	var veg_tiles =[2, 5, 8, 12, 15]
	return tile_id in veg_tiles

func _is_path(tile_id: int) -> bool:
	var path_tiles =[3, 7, 11]
	return tile_id in path_tiles

func _find_light_node() -> DirectionalLight2D:
	for child in tile_map.get_parent().get_children():
		if child is DirectionalLight2D:
			return child
	return null
