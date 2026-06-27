extends Node

enum BiomeTheme { JARDIN_CENTRAL, BOSQUE, LAGO, DESIERTO, TUNDRA, MONTAÑA }

var current_biome: String = "jardin-central"
var current_theme: BiomeTheme = BiomeTheme.JARDIN_CENTRAL
var emotional_state: String = "exploracion"
var master_bus: int
var music_bus: int
var sfx_bus: int
var ambient_bus: int
var crossfade_duration: float = 2.0

signal biome_changed(biome: String)
signal stem_adjusted(stem: String, db: float)

func initialize():
	master_bus = AudioServer.get_bus_index("Master")
	music_bus = AudioServer.get_bus_index("Music")
	sfx_bus = AudioServer.get_bus_index("SFX")
	ambient_bus = AudioServer.get_bus_index("Ambient")
	if music_bus == -1 or sfx_bus == -1 or ambient_bus == -1:
		_setup_buses()
	_setup_players()

func _setup_buses():
	var idx = AudioServer.bus_count
	AudioServer.add_bus(idx)
	AudioServer.set_bus_name(idx, "Music")
	music_bus = idx
	idx = AudioServer.bus_count
	AudioServer.add_bus(idx)
	AudioServer.set_bus_name(idx, "SFX")
	sfx_bus = idx
	idx = AudioServer.bus_count
	AudioServer.add_bus(idx)
	AudioServer.set_bus_name(idx, "Ambient")
	ambient_bus = idx

func _setup_players():
	if not has_node("AmbientPlayer"):
		var ap = AudioStreamPlayer.new()
		ap.name = "AmbientPlayer"
		ap.bus = "Ambient"
		ap.volume_db = -10
		add_child(ap)
	if not has_node("NewAmbientPlayer"):
		var nap = AudioStreamPlayer.new()
		nap.name = "NewAmbientPlayer"
		nap.bus = "Ambient"
		nap.volume_db = -80
		add_child(nap)

	var stem_configs = [
		["StemExploration", 220.0],
		["StemTension", 330.0],
		["StemJoy", 440.0],
		["StemMelancholy", 1760.0]
	]
	for cfg in stem_configs:
		var stem_name = cfg[0] as String
		var freq = cfg[1] as float
		if not has_node(stem_name):
			var player = AudioStreamPlayer.new()
			player.name = stem_name
			player.bus = "Music"
			player.volume_db = -80
			player.stream = _generate_tone(freq, 30.0)
			add_child(player)
			player.play()

func _generate_tone(freq: float, duration: float) -> AudioStreamWAV:
	var wav = AudioStreamWAV.new()
	wav.format = AudioStreamWAV.FORMAT_16_BITS
	wav.stereo = false
	wav.mix_rate = 44100
	var sample_count = int(44100.0 * duration)
	var data = PackedByteArray()
	data.resize(sample_count * 2)
	for i in sample_count:
		var sample = sin(i * TAU * freq / 44100.0) * 0.2
		var val = int(sample * 32767.0)
		data.encode_s16(i * 2, val)
	wav.loop_mode = AudioStreamWAV.LOOP_FORWARD
	wav.loop_begin = 0
	wav.loop_end = sample_count
	wav.data = data
	return wav

func transition_to_zone(zone_id: String):
	current_biome = zone_id
	var ambient_path = _get_ambient_path(zone_id)
	var ambient_player = get_node_or_null("AmbientPlayer") as AudioStreamPlayer
	var new_ambient = get_node_or_null("NewAmbientPlayer") as AudioStreamPlayer
	if not ambient_player or not new_ambient:
		biome_changed.emit(zone_id)
		return
	var stream = ResourceLoader.load(ambient_path)
	if not stream:
		biome_changed.emit(zone_id)
		return
	new_ambient.stream = stream
	new_ambient.play()
	var tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(ambient_player, "volume_db", -80, crossfade_duration)
	tween.tween_property(new_ambient, "volume_db", -10, crossfade_duration)
	await tween.finished
	ambient_player.stop()
	ambient_player.stream = new_ambient.stream
	ambient_player.volume_db = -10
	new_ambient.volume_db = -80
	new_ambient.stop()
	biome_changed.emit(zone_id)

func on_profile_updated(profile):
	if not profile:
		return
	var stems = {
		"StemExploration": profile.openness / 100.0,
		"StemTension": profile.neuroticism / 100.0,
		"StemJoy": profile.extraversion / 100.0,
		"StemMelancholy": 1.0 - (profile.agreeableness / 100.0)
	}
	for stem_name in stems:
		var player = get_node_or_null(stem_name) as AudioStreamPlayer
		if player:
			var target_db = stems[stem_name] * 50.0 - 45.0
			target_db = clamp(target_db, -80, 0)
			var tween = create_tween()
			tween.tween_property(player, "volume_db", target_db, 1.0)
			stem_adjusted.emit(stem_name, target_db)

func _get_ambient_path(zone_id: String) -> String:
	match zone_id:
		"jardin-central": return "res://assets/audio/ambient/jardin_central.ogg"
		"bosque": return "res://assets/audio/ambient/bosque.ogg"
		"lago": return "res://assets/audio/ambient/lago.ogg"
		"desierto": return "res://assets/audio/ambient/desierto.ogg"
		"tundra": return "res://assets/audio/ambient/tundra.ogg"
		"montaña": return "res://assets/audio/ambient/montana.ogg"
		_: return "res://assets/audio/ambient/jardin_central.ogg"

func play_sfx(sfx_path: String, volume: float = 0.0):
	var stream = ResourceLoader.load(sfx_path)
	if not stream:
		return
	var player = AudioStreamPlayer.new()
	player.bus = "SFX"
	player.stream = stream
	player.volume_db = volume
	add_child(player)
	player.play()
	await player.finished
	player.queue_free()

func set_master_volume(db: float):
	AudioServer.set_bus_volume_db(master_bus, db)

func set_music_volume(db: float):
	AudioServer.set_bus_volume_db(music_bus, db)

func set_sfx_volume(db: float):
	AudioServer.set_bus_volume_db(sfx_bus, db)
