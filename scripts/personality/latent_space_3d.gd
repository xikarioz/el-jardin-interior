extends Node

var _mean: Array = []
var _components: Array = []  # [3][17]
var _characters_3d: Array = []
var _loaded: bool = false

func initialize():
	var pca_file = FileAccess.open("res://scripts/personality/pca_3d_data.json", FileAccess.READ)
	if pca_file:
		var data = JSON.parse_string(pca_file.get_as_text())
		_mean = data["mean"]
		_components = data["components"]
		pca_file.close()
		_loaded = true
	
	var char_file = FileAccess.open("res://data/character-database-3d.json", FileAccess.READ)
	if char_file:
		_characters_3d = JSON.parse_string(char_file.get_as_text())
		char_file.close()

# Project 17 floats → Vector3
func project(profile_17: Array) -> Vector3:
	if not _loaded or profile_17.size() < 17:
		return Vector3.ZERO
	
	var centered = []
	for i in 17:
		centered.append(profile_17[i] - _mean[i])
	
	var result = Vector3.ZERO
	for i in 17:
		result.x += _components[0][i] * centered[i]
		result.y += _components[1][i] * centered[i]
		result.z += _components[2][i] * centered[i]
	
	return result

# Match: top_k nearest neighbors in 3D euclidean space
func match(query_3d: Vector3, top_k: int = 3, context: String = "") -> Array:
	var scored = []
	for ch in _characters_3d:
		if not ch.has("latent_3d"):
			continue
		var l = ch["latent_3d"]
		var pos = Vector3(l[0], l[1], l[2])
		var dist = query_3d.distance_to(pos)
		
		# Context bonus
		var bonus = 0.0
		var tags = ch.get("tags", [])
		if context == "exploracion" and "aventurero" in tags: bonus -= 0.3
		if context == "frustracion" and "perseverante" in tags: bonus -= 0.3
		if context == "tristeza" and "calido" in tags: bonus -= 0.3
		if context == "logro" and "inspirador" in tags: bonus -= 0.3
		
		scored.append({"character": ch, "distance": dist + bonus})
	
	scored.sort_custom(func(a, b): return a.distance < b.distance)
	
	# MMR diversity
	var selected = []
	for s in scored:
		var too_close = false
		for sel in selected:
			var p1 = Vector3(s.character["latent_3d"][0], s.character["latent_3d"][1], s.character["latent_3d"][2])
			var p2 = Vector3(sel.character["latent_3d"][0], sel.character["latent_3d"][1], sel.character["latent_3d"][2])
			if p1.distance_to(p2) < 1.0:
				too_close = true
				break
		if not too_close:
			selected.append(s)
		if selected.size() >= top_k:
			break
	
	return selected.map(func(s): return s.character)

func get_profile_3d() -> Vector3:
	var gm = get_node("/root/JardinCentral")
	if gm:
		var p = gm.get_personality().get_profile()
		if p:
			return project(p.to_vector())
	return Vector3.ZERO

func is_loaded() -> bool:
	return _loaded
