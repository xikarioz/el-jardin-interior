extends Node

func _ready():
	# Wait a frame, then render
	await get_tree().process_frame
	await get_tree().process_frame
	
	var image = get_viewport().get_texture().get_image()
	var timestamp = Time.get_unix_time_from_system()
	var path = "user://preview_%d.png" % timestamp
	image.save_png(path)
	print("Screenshot saved: ", path)
	get_tree().quit()
