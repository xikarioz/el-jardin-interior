extends Node2D


enum State { IDLE, APPROACH, PRESENT, QUESTION, LISTEN, REACT, DEPART, HIDDEN }
enum AnimalType { TORTOISE, FOX, OWL, BUTTERFLY, SNAIL, BIRD }

@export var animal_type: AnimalType
@export var companion_name: String = ""
@export var spawn_condition: String = ""
@export var spawn_threshold: float = 0.0
@export var move_speed: float = 120.0
@export var animations: Dictionary = {}

var state: State = State.HIDDEN
var target_position: Vector2 = Vector2.ZERO
var player_ref: Node2D = null
var dialog_queue: Array[String] = []
var is_moving: bool = false
var activation_radius: float = 200.0

signal state_changed(old_state: State, new_state: State)
signal question_asked(question: String)
signal dialog_closed()
signal interaction_completed(animal_type: int)

func _ready():
	visible = false
	_setup_animation_player()

func _setup_animation_player():
	if not has_node("AnimationPlayer"):
		var ap = AnimationPlayer.new()
		ap.name = "AnimationPlayer"
		add_child(ap)

func transition_to(new_state: State):
	var old = state
	state = new_state
	state_changed.emit(old, new_state)
	match state:
		State.IDLE:
			visible = true
			play_animation("idle")
		State.APPROACH:
			visible = true
			play_animation("walk")
			is_moving = true
			target_position = _get_approach_position()
		State.PRESENT:
			is_moving = false
			play_animation("present")
			await get_tree().create_timer(0.8).timeout
			transition_to(State.QUESTION)
		State.QUESTION:
			play_animation("idle")
			show_dialog()
		State.LISTEN:
			play_animation("listen")
		State.REACT:
			play_animation("react")
			await get_tree().create_timer(1.5).timeout
			transition_to(State.DEPART)
		State.DEPART:
			play_animation("walk")
			is_moving = true
			target_position = _get_depart_position()
		State.HIDDEN:
			visible = false
			is_moving = false

func _process(delta):
	if not is_moving or not visible:
		return
	var dir = target_position - global_position
	if dir.length() > 8.0:
		global_position += dir.normalized() * move_speed * delta
		_update_facing(dir)
	else:
		is_moving = false
		if state == State.APPROACH:
			transition_to(State.PRESENT)
		elif state == State.DEPART:
			transition_to(State.HIDDEN)

func _update_facing(direction: Vector2):
	if direction.x < 0:
		scale.x = -abs(scale.x)
	elif direction.x > 0:
		scale.x = abs(scale.x)

func _get_approach_position() -> Vector2:
	if player_ref:
		var offset = Vector2(80 + randi() % 60, -40 + randi() % 80)
		return player_ref.global_position + offset
	return global_position + Vector2(100, 0)

func _get_depart_position() -> Vector2:
	var angle = randf() * TAU
	return global_position + Vector2(cos(angle), sin(angle)) * 400

func move_to_player():
	is_moving = true
	target_position = _get_approach_position()

func show_dialog():
	if dialog_queue.is_empty():
		dialog_queue = _load_dialogs()
	if dialog_queue.is_empty():
		dialog_queue = _generate_dialog()
	var question = dialog_queue.pop_front()
	question_asked.emit(question)

func _load_dialogs() -> Array[String]:
	var gm = _get_game_manager()
	if gm and gm.has_method("get_dialog_loader"):
		var dl = gm.get_dialog_loader()
		var animal_id = _get_animal_id()
		return dl.get_random_dialogs(animal_id, 3)
	return []

func _get_animal_id() -> String:
	match animal_type:
		AnimalType.TORTOISE: return "tortuga"
		AnimalType.FOX: return "zorro"
		AnimalType.OWL: return "buho"
		AnimalType.BUTTERFLY: return "mariposa"
		AnimalType.SNAIL: return "caracol"
		AnimalType.BIRD: return "pajaro"
		_: return ""

func _generate_dialog() -> Array[String]:
	match animal_type:
		AnimalType.TORTOISE:
			return ["¿Cuántas flores ves?", "¿Puedes recordar este camino?", "Observa con calma..."]
		AnimalType.FOX:
			return ["¿Qué color tiene la hoja más grande?", "¡Sígueme!", "Encuentra la que es diferente"]
		AnimalType.OWL:
			return ["Escucha con atención...", "¿Qué sonido era ese?", "Repite la secuencia"]
		AnimalType.BUTTERFLY:
			return ["¿Cuál flor es más alta?", "¡A volar!", "¿Ves el patrón?"]
		AnimalType.SNAIL:
			return ["Toca despacio...", "¿Cuántos pasos?", "Siente el camino"]
		AnimalType.BIRD:
			return ["¡Canta conmigo!", "Repite esta melodía", "¿Qué nota sigue?"]
	return ["Hola..."]

func play_animation(anim_name: String):
	var ap = $AnimationPlayer as AnimationPlayer
	if ap and ap.has_animation(anim_name):
		ap.play(anim_name)

func on_player_answered(answer: Dictionary):
	transition_to(State.REACT)
	interaction_completed.emit(animal_type)

func on_interact():
	if state == State.IDLE or state == State.HIDDEN:
		if not player_ref:
			var players = get_tree().get_nodes_in_group("player")
			if players.size() > 0:
				player_ref = players[0] as Node2D
		summon(player_ref)

func check_spawn_condition(profile) -> bool:
	match spawn_condition:
		"calma":
			return profile.get("neuroticism", 0.5) < spawn_threshold
		"curiosidad":
			return profile.get("openness", 0.5) > spawn_threshold
		"persistencia":
			return _get_completed_tests() >= int(spawn_threshold * 100)
		"biome":
			return _get_unlocked_biomes() >= int(spawn_threshold * 10)
		_:
			return true

func _get_completed_tests() -> int:
	var gm = _get_game_manager()
	if gm:
		return gm.game_state.get("completed_tests", 0)
	return 0

func _get_unlocked_biomes() -> int:
	var gm = _get_game_manager()
	if gm:
		return gm.game_state.get("unlocked_biomes", []).size()
	return 0

func _get_game_manager():
	return get_tree().get_first_node_in_group("game_manager")

func can_activate(player_pos: Vector2) -> bool:
	if state != State.HIDDEN and state != State.IDLE:
		return false
	return global_position.distance_to(player_pos) <= activation_radius

func summon(player: Node2D):
	player_ref = player
	transition_to(State.APPROACH)
