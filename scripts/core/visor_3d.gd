extends Node3D

func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)

func _process(delta):
	# Slow auto-rotation of characters
	for child in get_children():
		if child is Node3D and child.name not in ["CameraPivot", "WorldEnvironment", "Sun", "Ambient", "Ground", "Camera3D"]:
			child.rotate_y(delta * 0.5)

func _input(event):
	var pivot = get_node_or_null("CameraPivot")
	if not pivot: return
	if event is InputEventMouseButton:
		var cam = pivot.get_node_or_null("Camera3D")
		if cam:
			if event.button_index == MOUSE_BUTTON_WHEEL_UP:
				cam.position.z = max(3.0, cam.position.z - 1.0)
			elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
				cam.position.z = min(20.0, cam.position.z + 1.0)
