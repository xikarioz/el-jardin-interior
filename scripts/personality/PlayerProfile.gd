extends RefCounted

var openness: float = 50.0
var conscientiousness: float = 50.0
var extraversion: float = 50.0
var agreeableness: float = 50.0
var neuroticism: float = 50.0
var atencion: float = 50.0
var control_inhibitorio: float = 50.0
var memoria_verbal: float = 50.0
var memoria_visoespacial: float = 50.0
var flexibilidad_cognitiva: float = 50.0
var razonamiento_analogico: float = 50.0
var velocidad_procesamiento: float = 50.0
var cognicion_social: float = 50.0
var estilo_aprendizaje: float = 50.0
var tolerancia_frustracion: float = 50.0
var impulsividad: float = 50.0
var creatividad: float = 50.0

func to_dict() -> Dictionary:
	return {
		"openness": openness, "conscientiousness": conscientiousness,
		"extraversion": extraversion, "agreeableness": agreeableness,
		"neuroticism": neuroticism, "atencion": atencion,
		"control_inhibitorio": control_inhibitorio, "memoria_verbal": memoria_verbal,
		"memoria_visoespacial": memoria_visoespacial, "flexibilidad_cognitiva": flexibilidad_cognitiva,
		"razonamiento_analogico": razonamiento_analogico, "velocidad_procesamiento": velocidad_procesamiento,
		"cognicion_social": cognicion_social, "estilo_aprendizaje": estilo_aprendizaje,
		"tolerancia_frustracion": tolerancia_frustracion, "impulsividad": impulsividad,
		"creatividad": creatividad
	}

func from_dict(data: Dictionary):
	for key in data:
		if key in self:
			set(key, data[key])
	return self

func to_vector() -> Array:
	return [
		openness, conscientiousness, extraversion, agreeableness, neuroticism,
		atencion, control_inhibitorio, memoria_verbal, memoria_visoespacial,
		flexibilidad_cognitiva, razonamiento_analogico, velocidad_procesamiento, cognicion_social,
		estilo_aprendizaje, tolerancia_frustracion, impulsividad, creatividad
	]

func adjust(prop, delta):
	if prop in self:
		var current = get(prop)
		set(prop, clamp(current + delta, 0.0, 100.0))
