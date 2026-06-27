extends Node

const PRESET_ANDROID ="Android"
const PRESET_IOS ="iOS"
const EXPORT_DIR ="export"
const ANDROID_APK ="el-jardin-interior.apk"
const IOS_DIR ="ios"

signal export_started(platform: String)
signal export_completed(platform: String, path: String)
signal export_failed(platform: String, error: String)

func export_android() -> void:
	export_started.emit("android")

	var preset = _find_preset(PRESET_ANDROID)
	if preset == null:
		export_failed.emit("android", "Android preset no encontrado")
		return

	_make_export_dir()
	var output_path = EXPORT_DIR.path_join(ANDROID_APK)

	var result = EditorInterface.export_project(preset, output_path)
	if result == OK:
		print("📱 APK generado en %s" % output_path)
		export_completed.emit("android", output_path)
	else:
		export_failed.emit("android", "Error codigo %d" % result)

func export_ios() -> void:
	export_started.emit("ios")

	var preset = _find_preset(PRESET_IOS)
	if preset == null:
		export_failed.emit("ios", "iOS preset no encontrado")
		return

	_make_export_dir()
	var ios_export_path =EXPORT_DIR.path_join(IOS_DIR)
	var result = EditorInterface.export_project(preset, ios_export_path)

	if result == OK:
		print("🍎 Proyecto Xcode en %s/" % ios_export_path)
		export_completed.emit("ios", ios_export_path)
	else:
		export_failed.emit("ios", "Error codigo %d" % result)

func export_both() -> void:
	await export_android()
	await export_ios()
	print("✅ Build multiplataforma completado")

func _find_preset(preset_name: String):
	var presets = EditorInterface.get_export_presets()
	for p in presets:
		if p.preset_name == preset_name:
			return p
	return null

func _make_export_dir() -> void:
	var dir =DirAccess.open("res://")
	if dir:
		dir.make_dir_recursive(EXPORT_DIR)
