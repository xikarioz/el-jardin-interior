extends Node

var dialog_banks: Dictionary = {}

signal dialog_loaded(animal_id: String, lines: Array[String])
signal dialog_closed()

func initialize() -> void:
	_load_dialog_banks()

func _load_dialog_banks() -> void:
	var dir = DirAccess.open("res://data/")
	if not dir:
		return
	dir.list_dir_begin()
	var file_name = dir.get_next()
	while file_name != "":
		if file_name.ends_with(".json"):
			var path = "res://data/" + file_name
			var file = FileAccess.open(path, FileAccess.READ)
			if file:
				var json = JSON.parse_string(file.get_as_text())
				if json is Dictionary:
					_register_bank(json)
				file.close()
		file_name = dir.get_next()

func _register_bank(data: Dictionary) -> void:
	if data.has("dialogos") and data.dialogos is Dictionary:
		for animal_id in data.dialogos:
			var lines = data.dialogos[animal_id]
			if lines is Array:
				if not dialog_banks.has(animal_id):
					dialog_banks[animal_id] = []
				dialog_banks[animal_id].append_array(lines)

func get_dialogs(animal_id: String) -> Array[String]:
	return dialog_banks.get(animal_id, []).duplicate()

func get_random_dialogs(animal_id: String, count: int = 3) -> Array[String]:
	var all = get_dialogs(animal_id)
	if all.is_empty():
		return ["Hola..."]
	all.shuffle()
	if all.size() > count:
		all = all.slice(0, count)
	return all
