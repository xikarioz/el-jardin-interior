extends Node

func extract_features(event) -> Dictionary:
	if event == null:
		return _default_features()

	var hits = event.get("hits", 0)
	var misses = event.get("misses", 0)
	var fas = event.get("false_alarms", 0)
	var total = max(hits + misses + fas, 1)

	var accuracy = float(hits) / total
	var reaction_time = event.get("reaction_time", 0.0)
	var attempts = event.get("attempts", 1)

	var strategy = _detect_strategy(reaction_time, accuracy, attempts)
	var strategy_score = _calc_strategy_score(reaction_time, accuracy, attempts)

	return {
		"reaction_time": reaction_time,
		"accuracy": accuracy,
		"strategy": strategy,
		"strategy_score": strategy_score,
		"attempts": attempts,
		"zone": event.get("zone_id", ""),
		"animal_interaction": event.get("animal_id", "")
	}

func _default_features() -> Dictionary:
	return {
		"reaction_time": 0.0, "accuracy": 0.0,
		"strategy": "neutral", "strategy_score": 0.0,
		"attempts": 0, "zone": "", "animal_interaction": ""
	}

func _detect_strategy(rt, acc, attempts) -> String:
	if attempts > 5: return "exploratory"
	if attempts <= 2: return "decisive"
	if rt < 2.0 and acc >= 0.7: return "fast_accurate"
	if rt < 2.0 and acc < 0.7: return "fast_inaccurate"
	if rt >= 2.0 and acc >= 0.7: return "cautious_accurate"
	return "cautious_inaccurate"

func _calc_strategy_score(rt, acc, attempts) -> float:
	var base = acc / max(0.1, rt + 0.5) * 10.0
	var attempt_penalty = clamp(1.0 - (attempts - 1) * 0.05, 0.7, 1.0)
	return clamp(base * attempt_penalty, 0.0, 10.0)

func initialize():
	pass
