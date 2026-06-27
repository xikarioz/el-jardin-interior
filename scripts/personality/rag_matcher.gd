
const CHARACTER_DB_PATH ="res://data/character-database.json"
const PATIENT_DIMS =17
const CHAR_DIMS =13

var _characters: Array = []
var _char_embeddings: Array = []
var _char_norms: Array = []
var _loaded =false

func _ready() -> void:
	_load_database()

func _load_database() -> void:
	var file =FileAccess.open(CHARACTER_DB_PATH, FileAccess.READ)
	if file == null:
		push_error("RAGMatcher: no se pudo cargar character-database.json")
		return

	var json_str =file.get_as_text()
	var json =JSON.new()
	var err =json.parse(json_str)
	if err != OK:
		push_error("RAGMatcher: error parsing JSON: ", err)
		return

	var data = json.data
	if data is Array:
		_characters = data
	elif data is Dictionary and data.has("characters"):
		_characters = data["characters"]
	else:
		push_error("RAGMatcher: formato de JSON inesperado")
		return

	_precompute_embeddings()
	_loaded = true

func _precompute_embeddings() -> void:
	_char_embeddings.clear()
	_char_norms.clear()
	for ch in _characters:
		var emb =_char_to_vector(ch)
		_char_embeddings.append(emb)
		_char_norms.append(_norm(emb))

func _char_to_vector(char_data: Dictionary) -> Array:
	var res: Array = []
	res.resize(CHAR_DIMS)

	res[0] = float(char_data.get("openness", 0.0))
	res[1] = float(char_data.get("conscientiousness", 0.0))
	res[2] = float(char_data.get("extraversion", 0.0))
	res[3] = float(char_data.get("agreeableness", 0.0))
	res[4] = float(char_data.get("neuroticism", 0.0))

	res[5] = float(char_data.get("memoria", 0.0))
	res[6] = float(char_data.get("atencion", 0.0))
	res[7] = float(char_data.get("planificacion", 0.0))
	res[8] = float(char_data.get("flexibilidad", 0.0))
	res[9] = float(char_data.get("inhibicion", 0.0))
	res[10] = float(char_data.get("velocidad_procesamiento", 0.0))
	res[11] = float(char_data.get("toma_decisiones", 0.0))
	res[12] = float(char_data.get("razonamiento", 0.0))

	return res

func _norm(v: Array) -> float:
	var s =0.0
	for val in v:
		s += val * val
	return sqrt(s)

func _dot(a: Array, b: Array) -> float:
	var s =0.0
	for i in range(min(a.size(), b.size())):
		s += a[i] * b[i]
	return s

func _cosine_similarity(a: Array, b: Array, norm_a: float, norm_b: float) -> float:
	if norm_a < 1e-8 or norm_b < 1e-8:
		return 0.0
	return _dot(a, b) / (norm_a * norm_b)

func _mmr_diversity(selected: Array, candidates: Array, lambda_val: float = 0.6) -> int:
	var best_idx =-1
	var best_score =-INF

	for i in candidates.size():
		if candidates[i].selected:
			continue

		var c = candidates[i]
		var rel_score =c.similarity
		var max_div =0.0

		for sel in selected:
			var sim =_cosine_similarity(
				_char_embeddings[c.index],
				_char_embeddings[sel.index],
				_char_norms[c.index],
				_char_norms[sel.index]
			)
			if sim > max_div:
				max_div = sim

		var mmr =lambda_val * rel_score - (1.0 - lambda_val) * max_div
		if mmr > best_score:
			best_score = mmr
			best_idx = i

	return best_idx

func _project_context_vector(context: String) -> Array:
	var ctx_lower =context.to_lower()
	var vec: Array = []
	vec.resize(PATIENT_DIMS)
	vec.fill(0.0)

	if "triste" in ctx_lower:
		vec[4] += 1.5
		vec[3] += 0.5
	elif "ansiedad" in ctx_lower or "miedo" in ctx_lower:
		vec[4] += 2.0
		vec[1] += 0.8
	elif "rabia" in ctx_lower or "enojo" in ctx_lower:
		vec[3] -= 1.0
		vec[4] += 1.0
	elif "alegria" in ctx_lower or "feliz" in ctx_lower:
		vec[2] += 1.0
		vec[3] += 0.8
	elif "soledad" in ctx_lower:
		vec[2] -= 1.0
		vec[3] += 0.6

	return vec

func match(player_vector: Array, context: String = "", top_k: int = 3) -> Array:
	if not _loaded:
		_load_database()
		if not _loaded:
			return []

	if player_vector.size() < CHAR_DIMS:
		push_error("RAGMatcher: player_vector demasiado corto")
		return []

	var player_trunc =player_vector.slice(0, CHAR_DIMS)
	var player_norm =_norm(player_trunc)

	var ctx_bias =_project_context_vector(context)

	var candidates: Array = []
	candidates.resize(_characters.size())

	for i in _characters.size():
		var biased =player_trunc.duplicate()
		if context.length() > 0:
			for j in min(biased.size(), ctx_bias.size()):
				biased[j] += ctx_bias[j] * 0.3

		var sim =_cosine_similarity(biased, _char_embeddings[i], player_norm, _char_norms[i])
		candidates[i] = {
			"index": i,
			"similarity": sim,
			"selected": false
		}

	candidates.sort_custom(func(a, b): return a.similarity > b.similarity)

	var selected: Array = []
	for _k in range(min(top_k, _characters.size())):
		var idx =_mmr_diversity(selected, candidates, 0.6)
		if idx < 0:
			break
		candidates[idx].selected = true
		var ch_idx =candidates[idx].index
		var ch =_characters[ch_idx].duplicate()
		ch["_score"] = candidates[idx].similarity
		ch.erase("personality_vector") if ch.has("personality_vector") else null
		ch.erase("gender") if ch.has("gender") else null
		selected.append(ch)

	return selected

func match_by_id(player_vector: Array, preferred_id: String) -> Dictionary:
	if not _loaded:
		return {}

	for i in _characters.size():
		var ch =_characters[i]
		if str(ch.get("id", "")) == preferred_id or str(ch.get("name", "")) == preferred_id:
			var player_trunc =player_vector.slice(0, CHAR_DIMS)
			var pn =_norm(player_trunc)
			var sim =_cosine_similarity(player_trunc, _char_embeddings[i], pn, _char_norms[i])
			var result =ch.duplicate()
			result["_score"] = sim
			result.erase("gender") if result.has("gender") else null
			return result
	return {}

func get_character_count() -> int:
	return _characters.size()
