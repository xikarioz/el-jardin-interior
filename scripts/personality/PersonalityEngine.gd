extends Node

var _profile = null
var _feature_extractor = null
var _nn = null

const ONNX_PATH = "res://data/personality_rf.onnx"

func initialize():
	if _profile == null:
		var PlayerProfileClass = load("res://scripts/personality/PlayerProfile.gd")
		if PlayerProfileClass:
			_profile = PlayerProfileClass.new()

	var fe_script = load("res://scripts/personality/feature_extractor.gd")
	if fe_script and _feature_extractor == null:
		_feature_extractor = fe_script.new()

	var nn_script = load("res://scripts/personality/nn_adaptativa.gd")
	if nn_script and _nn == null:
		_nn = nn_script.new()
		if _nn.has_method("load"):
			_nn.load("user://nn_weights.json")

	load_onnx()

func register_result(result):
	if not _profile or not _feature_extractor:
		initialize()
		if not _feature_extractor:
			return

	var features = _feature_extractor.extract_features(result)

	_profile.impulsividad = clamp(_profile.impulsividad + features.reaction_time * 0.1, 0.0, 100.0)
	_profile.velocidad_procesamiento = clamp(_profile.velocidad_procesamiento + features.accuracy * 5.0, 0.0, 100.0)
	_profile.tolerancia_frustracion = clamp(_profile.tolerancia_frustracion - features.strategy_score * 0.5, 0.0, 100.0)

	match features.strategy:
		"fast_accurate":
			_profile.atencion = clamp(_profile.atencion + 1.0, 0.0, 100.0)
		"cautious_inaccurate":
			_profile.control_inhibitorio = clamp(_profile.control_inhibitorio + 1.5, 0.0, 100.0)
		"exploratory":
			_profile.creatividad = clamp(_profile.creatividad + 1.0, 0.0, 100.0)
		"decisive":
			_profile.razonamiento_analogico = clamp(_profile.razonamiento_analogico + 0.8, 0.0, 100.0)

	if _nn:
		var input_vec = _profile.to_vector()
		if _nn.has_method("adjust_positive"):
			_nn.adjust_positive(input_vec)
		if _nn.has_method("save"):
			_nn.save("user://nn_weights.json")

func get_profile():
	if _profile == null:
		initialize()
	return _profile

func get_nn():
	return _nn

func load_onnx():
	if ResourceLoader.exists(ONNX_PATH):
		print("ONNX model found at ", ONNX_PATH)
		var file = FileAccess.open(ONNX_PATH, FileAccess.READ)
		if file:
			var size = file.get_length()
			print("ONNX model size: ", size, " bytes")
			file.close()
	else:
		print("ONNX model not found — skipping")
