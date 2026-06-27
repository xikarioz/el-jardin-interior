extends Node


enum Gesture { NONE, TAP, SWIPE, HOLD, PINCH, ZOOM }

var touch_start: Vector2 = Vector2.ZERO
var touch_current: Vector2 = Vector2.ZERO
var touch_time: float = 0.0
var is_touching: bool = false
var hold_threshold: float = 0.4
var swipe_threshold: float = 30.0
var zoom_threshold: float = 10.0
var long_press_time: float = 0.0
var long_press_triggered: bool = false
var hold_zoom_speed: float = 0.005
var last_hold_position: Vector2 = Vector2.ZERO

var pinch_start_distance: float = 0.0
var pinch_initial: Dictionary = {}

var screen_size: Vector2 = Vector2(2732, 2048)

signal tapped(position: Vector2, target: Node)
signal swiped(direction: Vector2, velocity: Vector2)
signal hold_started(position: Vector2)
signal hold_ended(position: Vector2)
signal zoomed(factor: float)
signal interacted(target: Node)
signal movement_requested(position: Vector2)

func _input(event):
	if event is InputEventScreenTouch:
		_handle_touch(event)
	elif event is InputEventScreenDrag:
		_handle_drag(event)
	elif event is InputEventMagnifyGesture:
		_handle_pinch(event)

func _handle_touch(event: InputEventScreenTouch):
	if event.pressed:
		touch_start = event.position
		touch_current = event.position
		touch_time = 0.0
		long_press_time = 0.0
		long_press_triggered = false
		is_touching = true
	else:
		is_touching = false
		if not long_press_triggered:
			var dist = touch_start.distance_to(event.position)
			var target = _get_target_at(touch_start)
			if dist < swipe_threshold:
				tapped.emit(touch_start, target)
				if target:
					interacted.emit(target)
				else:
					movement_requested.emit(touch_start)
			else:
				var dir = (event.position - touch_start).normalized()
				var vel = (event.position - touch_start) / max(touch_time, 0.016)
				swiped.emit(dir, vel)
		if long_press_triggered:
			hold_ended.emit(event.position)

func _handle_drag(event: InputEventScreenDrag):
	touch_current = event.position
	touch_time += get_process_delta_time()
	if touch_time >= hold_threshold and not long_press_triggered:
		long_press_triggered = true
		hold_started.emit(event.position)
		last_hold_position = event.position
	elif long_press_triggered:
		var delta_y = event.position.y - last_hold_position.y
		if abs(delta_y) > 2.0:
			var factor = 1.0 - delta_y * hold_zoom_speed
			factor = clamp(factor, 0.5, 2.0)
			zoomed.emit(factor)
		last_hold_position = event.position

func _handle_pinch(event: InputEventMagnifyGesture):
	zoomed.emit(event.factor)

func _get_target_at(pos: Vector2) -> Node:
	var space = get_viewport().world_2d.direct_space_state
	if not space:
		return null
	var params = PhysicsPointQueryParameters2D.new()
	params.position = pos
	params.collide_with_areas = true
	params.collide_with_bodies = true
	var results = space.intersect_point(params)
	for r in results:
		var collider = r.collider
		if collider and collider.has_method("on_interact"):
			return collider
		if collider and collider.get_parent() and collider.get_parent().has_method("on_interact"):
			return collider.get_parent()
	return null

func get_touch_delta() -> Vector2:
	return touch_current - touch_start

func is_holding() -> bool:
	return is_touching and touch_time >= hold_threshold
