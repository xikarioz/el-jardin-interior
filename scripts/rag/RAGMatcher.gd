extends Node

func initialize():
	pass

func match_characters(player_vector: Array, context: String = "", top_k: int = 3) -> Array:
	var gm = get_node("/root/JardinCentral")
	if not gm:
		return []
	
	var latent = gm.get_latent_space()
	if not latent or not latent.is_loaded():
		return []
	
	var query_3d = latent.project(player_vector)
	return latent.match(query_3d, top_k, context)

func on_test_completed(result: Dictionary):
	var features = _extract_features(result)
	if features.is_empty():
		return
	var vec = _features_to_vector(features)
	var matches = match_characters(vec, result.get("context", ""), 3)
	print("RAGMatcher 3D: ", matches.size(), " personajes cercanos")

func _extract_features(result: Dictionary) -> Dictionary:
	var fe = load("res://scripts/personality/feature_extractor.gd").new()
	return fe.extract_features(result)

func _features_to_vector(features: Dictionary) -> Array:
	var gm = get_node("/root/JardinCentral")
	if gm and gm.get_personality() and gm.get_personality().get_profile():
		return gm.get_personality().get_profile().to_vector()
	var vec = []
	vec.resize(17)
	for i in 17:
		vec[i] = 50.0
	return vec
