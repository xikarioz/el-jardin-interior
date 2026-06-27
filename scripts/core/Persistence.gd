extends Node

var _auto_save_timer: Timer

func _ready():
	_setup_auto_save()

func _setup_auto_save():
	_auto_save_timer = Timer.new()
	_auto_save_timer.name = "AutoSaveTimer"
	_auto_save_timer.wait_time = 300.0
	_auto_save_timer.one_shot = false
	_auto_save_timer.timeout.connect(_on_auto_save)
	add_child(_auto_save_timer)
	_auto_save_timer.start()

func _on_auto_save():
	for slot in range(3):
		save_game(slot)

func save_game(slot: int) -> bool:
	var path = "user://save_%d.dat" % slot
	var dict = _build_save_dict()
	dict["slot"] = slot
	var bytes = var_to_bytes(dict)
	var compressed = bytes.compress(FileAccess.COMPRESSION_GZIP)
	var file = FileAccess.open(path, FileAccess.WRITE)
	if file:
		file.store_32(compressed.size())
		file.store_buffer(compressed)
		file.close()
		return true
	return false

func load_game(slot: int) -> Dictionary:
	var path = "user://save_%d.dat" % slot
	if not FileAccess.file_exists(path):
		return {}
	var file = FileAccess.open(path, FileAccess.READ)
	if file:
		var size = file.get_32()
		var compressed = file.get_buffer(size)
		file.close()
		if compressed.is_empty():
			return {}
		var bytes = compressed.decompress(10485760, FileAccess.COMPRESSION_GZIP)
		if bytes.is_empty():
			return {}
		var data = bytes_to_var(bytes)
		if data is Dictionary:
			return data
	return {}

func _build_save_dict() -> Dictionary:
	var result = {
		"version": "1.0",
		"timestamp": Time.get_unix_time_from_system(),
		"game_state": {},
		"profile": {},
		"current_zone": "",
		"current_animal": "",
		"save_slot": 0
	}
	var gm = _get_game_manager()
	if gm:
		result["game_state"] = gm.game_state
		result["current_zone"] = gm.current_zone
		result["current_animal"] = gm.current_animal
		result["save_slot"] = gm.save_slot
		result["total_tests"] = gm.game_state.get("total_tests", 0)
		result["completed_tests"] = gm.game_state.get("completed_tests", 0)
		var p = gm.get_personality().get_profile()
		if p and p.has_method("to_dict"):
			result["profile"] = p.to_dict()
	return result

func _get_game_manager():
	var group = get_tree().get_first_node_in_group("game_manager")
	if group:
		return group
	return null

func get_slot_info(slot: int) -> Dictionary:
	var data = load_game(slot)
	if data.is_empty():
		return {"exists": false, "slot": slot}
	return {
		"exists": true,
		"slot": slot,
		"timestamp": data.get("timestamp", 0),
		"play_time": data.get("game_state", {}).get("play_time", 0.0),
		"biomes": data.get("game_state", {}).get("unlocked_biomes", []),
		"completed_tests": data.get("completed_tests", 0),
		"version": data.get("version", "")
	}

func delete_slot(slot: int) -> bool:
	var path = "user://save_%d.dat" % slot
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(path)
		return true
	return false
