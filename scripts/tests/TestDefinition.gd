extends Resource


enum MechanicType { FLANKER, STROOP, CORSI, SPAN, N_BACK, MATRIX, CATEGORY, GO_NOGO, SHAPE_SORT, TRAIL_MAKING, ODDBALL, TASK_SWITCH, VISUAL_SEARCH, FIVE_CHOICE, STOP_SIGNAL, CHANGE_DETECTION, MENTAL_ROTATION, EMBODIED_SORT, FLOWER_COUNT, BIRD_MEMO, SHELL_HIDE, ROCK_PAIRS, LEAF_SEQUENCE, BUG_STROOP, PATH_FIND, WATER_SPAN, SEED_MATCH, SHADOW_SORT, BREATH_COUNT, MELODY_MEMO, SOCIAL_CUE, EMOTION_MATCH, TURN_TAKE, SYMMETRY, FRACTION_GARDEN, MEMO_GROVE, PATTERN_PAVE, TREE_SPAN, NECTAR_N_BACK, POLLEN_STROOP, ROOT_MATRIX, COMPASS_FLANKER, GARDEN_SPAN, CROP_CATEGORY, BLOOM_STROOP, HARVEST_GO, PRUNE_NOGO, MUSHROOM_MATCH, MOSS_TRAIL, FERN_ODDBALL, SPORE_SWITCH, PETAL_SEARCH, STEM_CHOICE, VINE_STOP, BUD_CHANGE, SEED_ROTATION, GROVE_SORT, POND_COUNT, NEST_MEMO, BURROW_HIDE, PEBBLE_PAIRS, VINE_SEQUENCE, PETAL_STROOP, ROOT_PATH, DEW_SPAN, LEAF_MATCH, CLOUD_SORT, RHYTHM_COUNT, TONE_MEMO, GLANCE_CUE, SMILE_MATCH, SHARE_TAKE, WING_SYMMETRY, SPORE_MATRIX, ANTLER_FLANKER, HIVE_SPAN, DEN_CATEGORY, SHELL_SORT, WEB_GO, WORM_NOGO, ACORN_MATCH, BRANCH_TRAIL, SAP_ODDBALL, TWIG_SWITCH, BLOOM_SEARCH, FLIGHT_CHOICE, TIDEPOOL_STOP, ECHO_CHANGE, DRIFT_ROTATION, TIDAL_SORT, KELP_COUNT, REEF_MEMO, CRAB_HIDE, CORAL_PAIRS, CURRENT_SEQUENCE, WAVE_STROOP, DUNE_PATH, OASIS_SPAN, CACTUS_MATCH, MIRAGE_SORT, SAND_RHYTHM, STAR_MEMO, DUST_SWITCH, OASIS_SEARCH, DUNE_CHOICE, MIRAGE_STOP, FOSSIL_CHANGE, DUNE_ROTATION, CANOPY_SORT, VINE_COUNT, FERN_MEMO, MOSSY_HIDE, TRUNK_PAIRS, ROOT_SEQUENCE, SAP_STROOP, BARK_PATH, NECTAR_SPAN, ORCHID_MATCH, FUNGUS_SORT, CRAWLER_GO, SLIME_NOGO, SPORE_MATCH, SOIL_TRAIL, COMPOST_ODDBALL, PETAL_SWITCH }

@export var id: String
@export var mechanic_type: MechanicType
@export var min_age: int
@export var max_age: int
@export var difficulty: int
@export var biome: String
@export var instructions: String
@export var time_limit: float = 0.0
@export var trials: int = 10
@export var stimuli_pool: Array[String] = []
@export var reward_scene: String = ""
@export var personality_weights: Dictionary = {
	"atencion": 0.0,
	"control_inhibitorio": 0.0,
	"memoria_verbal": 0.0,
	"memoria_visoespacial": 0.0,
	"flexibilidad_cognitiva": 0.0,
	"velocidad_procesamiento": 0.0
}
@export var target_cognitive_domain: String = ""
@export var adaptive_difficulty: bool = false
@export var min_difficulty: int = 1
@export var max_difficulty: int = 5

func _init(p_id: String = "", p_type: MechanicType = MechanicType.FLANKER, p_min: int = 4, p_max: int = 12, p_diff: int = 1, p_biome: String = "jardin-central", p_instructions: String = ""):
	id = p_id
	mechanic_type = p_type
	min_age = p_min
	max_age = p_max
	difficulty = p_diff
	biome = p_biome
	instructions = p_instructions

func get_difficulty_label() -> String:
	match difficulty:
		1: return "semilla"
		2: return "brote"
		3: return "flor"
		4: return "arbol"
		5: return "bosque"
		_: return "semilla"

func is_applicable_for(age: int) -> bool:
	return age >= min_age and age <= max_age

func get_cognitive_weight(domain: String) -> float:
	return personality_weights.get(domain, 0.0)
