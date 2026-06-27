extends Node



var available_tests: Dictionary = {}
var test_history: Array[Dictionary] = []
var current_test = null
var tests_by_biome: Dictionary = {}
var tests_by_type: Dictionary = {}

signal test_started(test_id: String)
signal test_completed(test_id: String, result: Dictionary)
signal test_failed(test_id: String, error: String)

func _ready():
	_load_all_tests()

func _load_all_tests():
	var dir = DirAccess.open("res://data/tests/")
	if not dir:
		return
	dir.list_dir_begin()
	var file_name = dir.get_next()
	while file_name != "":
		if file_name.ends_with(".tres") or file_name.ends_with(".res"):
			var path = "res://data/tests/" + file_name
			var test_def = load(path) 
			if test_def:
				_register_test(test_def)
		file_name = dir.get_next()

func _register_test(test_def):
	available_tests[test_def.id] = test_def
	if not tests_by_biome.has(test_def.biome):
		tests_by_biome[test_def.biome] = []
	tests_by_biome[test_def.biome].append(test_def)
	if not tests_by_type.has(test_def.mechanic_type):
		tests_by_type[test_def.mechanic_type] = []
	tests_by_type[test_def.mechanic_type].append(test_def)

func start_test(test_id: String) :
	if not available_tests.has(test_id):
		test_failed.emit(test_id, "test_not_found")
		return null
	current_test = available_tests[test_id]
	test_started.emit(test_id)
	return current_test

func report_result(test_id: String, result: Dictionary):
	var gm = _get_game_manager()
	var profile_snapshot = {}
	if gm and gm.has_method("get_personality"):
		var p = gm.get_personality().get_profile()
		if p and p.has_method("to_dict"):
			profile_snapshot = p.to_dict()
	var entry = {
		"test_id": test_id,
		"result": result,
		"timestamp": Time.get_unix_time_from_system(),
		"profile_snapshot": profile_snapshot
	}
	test_history.append(entry)
	test_completed.emit(test_id, result)
	if gm and gm.has_method("on_test_completed"):
		gm.on_test_completed(result)

func _get_game_manager():
	return get_tree().get_first_node_in_group("game_manager")

func get_tests_for_age(age: int) -> Array:
	var result: Array = []
	for test in available_tests.values():
		if test.is_applicable_for(age):
			result.append(test)
	return result

func get_tests_for_biome(biome: String) -> Array:
	return tests_by_biome.get(biome, []).duplicate()

func get_tests_by_type(mechanic_type):
	return tests_by_type.get(mechanic_type, []).duplicate()

func get_test_count() -> int:
	return available_tests.size()

func get_completed_count() -> int:
	var gm = _get_game_manager()
	if gm:
		return gm.game_state.get("completed_tests", 0)
	return 0

func get_recent_results(limit: int = 10) -> Array[Dictionary]:
	var recent = test_history.duplicate()
	recent.reverse()
	return recent.slice(0, limit)

func get_stats() -> Dictionary:
	return {
		"total": get_test_count(),
		"completed": get_completed_count(),
		"history_size": test_history.size()
	}

func extract_test_features(test_id: String, result: Dictionary) -> Dictionary:
	var gm = _get_game_manager()
	if gm and gm.has_method("get_feature_extractor"):
		var fe = gm.get_feature_extractor()
		var event = {
			"hits": result.get("hits", 0),
			"misses": result.get("misses", 0),
			"false_alarms": result.get("false_alarms", 0),
			"reaction_time": result.get("avg_reaction_time", 0.0),
			"attempts": result.get("attempts", 1),
			"zone_id": result.get("zone_id", ""),
			"animal_id": result.get("animal_id", "")
		}
		return fe.extract_features(event)
	return {}
