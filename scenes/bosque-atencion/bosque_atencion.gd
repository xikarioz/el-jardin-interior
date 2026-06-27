extends Node2D

var tree_data: Array[Dictionary] = []
var bush_data: Array[Dictionary] = []
var flower_data: Array[Dictionary] = []
var grass_data: Array[Dictionary] = []
var mushroom_data: Array[Dictionary] = []

const TRUNK_COLOR := Color(0.45, 0.25, 0.12)
const LEAF_COLORS := [
	Color(0.2, 0.55, 0.15),
	Color(0.25, 0.6, 0.12),
	Color(0.15, 0.5, 0.1),
	Color(0.3, 0.65, 0.18),
	Color(0.22, 0.58, 0.08),
]
const BUSH_COLORS := [
	Color(0.18, 0.5, 0.12),
	Color(0.22, 0.55, 0.15),
	Color(0.15, 0.45, 0.1),
]
const FLOWER_COLORS := [
	Color(1, 0.3, 0.3),
	Color(1, 0.8, 0.2),
	Color(0.9, 0.2, 0.8),
	Color(0.3, 0.5, 1.0),
	Color(1, 0.5, 0.1),
	Color(1, 1, 1),
]
const GRASS_COLOR := Color(0.25, 0.55, 0.1)
const MUSHROOM_CAP := Color(0.9, 0.5, 0.15)
const MUSHROOM_STALK := Color(0.95, 0.9, 0.8)

func _ready():
	_generate_trees()
	_generate_bushes()
	_generate_flowers()
	_generate_grass()
	_generate_mushrooms()
	queue_redraw()

func _generate_trees():
	for i in range(12):
		var x := 100 + (i * 160) + randi() % 80
		var trunk_h := 40 + randi() % 30
		var trunk_w := 6 + randi() % 4
		var canopy_r := 30 + randi() % 25
		var leaf := LEAF_COLORS[randi() % LEAF_COLORS.size()]
		tree_data.append({
			pos = Vector2(x, 440 - trunk_h),
			trunk_h = trunk_h,
			trunk_w = trunk_w,
			canopy_r = canopy_r,
			color = leaf,
			trunk_color = Color(TRUNK_COLOR.r + randf() * 0.1, TRUNK_COLOR.g + randf() * 0.1, TRUNK_COLOR.b, 1),
		})

func _generate_bushes():
	for i in range(8):
		bush_data.append({
			pos = Vector2(60 + (i * 240) + randi() % 100, 460 + randi() % 20),
			radius = 12 + randi() % 15,
			color = BUSH_COLORS[randi() % BUSH_COLORS.size()],
		})

func _generate_flowers():
	for i in range(15):
		flower_data.append({
			pos = Vector2(50 + (i * 130) + randi() % 60, 445 + randi() % 30),
			petal_r = 3 + randi() % 3,
			color = FLOWER_COLORS[randi() % FLOWER_COLORS.size()],
		})

func _generate_grass():
	for i in range(40):
		grass_data.append({
			pos = Vector2(20 + (i * 50) + randi() % 30, 470 + randi() % 15),
			height = 6 + randi() % 10,
			lean = (randf() - 0.5) * 0.4,
		})

func _generate_mushrooms():
	for i in range(5):
		mushroom_data.append({
			pos = Vector2(200 + (i * 350) + randi() % 80, 465 + randi() % 15),
			stalk_h = 6 + randi() % 4,
			cap_r = 5 + randi() % 4,
		})

func _draw():
	for t in tree_data:
		_draw_tree(t)
	for b in bush_data:
		_draw_bush(b)
	for f in flower_data:
		_draw_flower(f)
	for g in grass_data:
		_draw_grass(g)
	for m in mushroom_data:
		_draw_mushroom(m)

func _draw_tree(t: Dictionary):
	var x := t.pos.x
	var y := t.pos.y
	var tw := t.trunk_w
	var th := t.trunk_h
	var cr := t.canopy_r

	draw_rect(Rect2(x - tw / 2, y, tw, th), t.trunk_color)

	var canopy_top := y
	var p1 := Vector2(x, canopy_top - cr * 1.3)
	var p2 := Vector2(x - cr, canopy_top + cr * 0.3)
	var p3 := Vector2(x + cr, canopy_top + cr * 0.3)
	draw_colored_polygon(PackedVector2Array([p1, p2, p3]), t.color)

	var p4 := Vector2(x, canopy_top - cr * 0.85)
	var p5 := Vector2(x - cr * 0.75, canopy_top + cr * 0.5)
	var p6 := Vector2(x + cr * 0.75, canopy_top + cr * 0.5)
	var darker := t.color * 0.85
	draw_colored_polygon(PackedVector2Array([p4, p5, p6]), darker)

func _draw_bush(b: Dictionary):
	var pos := b.pos
	var r := b.radius
	var c := b.color
	draw_circle(pos + Vector2(-r * 0.3, r * 0.2), r * 0.7, c)
	draw_circle(pos + Vector2(r * 0.3, r * 0.15), r * 0.6, c)
	draw_circle(pos + Vector2(0, -r * 0.15), r * 0.65, c)
	var darker := c * 0.8
	draw_circle(pos + Vector2(-r * 0.2, -r * 0.25), r * 0.35, darker)
	draw_circle(pos + Vector2(r * 0.25, -r * 0.2), r * 0.3, darker)

func _draw_flower(f: Dictionary):
	var pos := f.pos
	var pr := f.petal_r
	var c := f.color

	var stem_top := pos + Vector2(0, -pr * 3)
	draw_line(stem_top, pos + Vector2(0, -pr * 7), Color(0.2, 0.5, 0.1), 1.5)

	for angle in range(0, 360, 60):
		var rad := deg_to_rad(angle)
		var px := stem_top.x + cos(rad) * pr * 1.5
		var py := stem_top.y + sin(rad) * pr * 1.5
		draw_circle(Vector2(px, py), pr, c)
	draw_circle(stem_top, pr * 0.7, Color(1, 0.9, 0.3))

	var highlight := c * 1.15
	for angle in range(0, 360, 120):
		var rad := deg_to_rad(angle)
		var px := stem_top.x + cos(rad) * pr
		var py := stem_top.y + sin(rad) * pr
		draw_circle(Vector2(px, py), pr * 0.5, highlight)

func _draw_grass(g: Dictionary):
	var pos := g.pos
	var h := g.height
	var lean := g.lean
	draw_line(pos, pos + Vector2(lean * h, -h), GRASS_COLOR, 1.5)

func _draw_mushroom(m: Dictionary):
	var pos := m.pos
	var sh := m.stalk_h
	var cr := m.cap_r
	draw_rect(Rect2(pos.x - cr * 0.25, pos.y - sh, cr * 0.5, sh), MUSHROOM_STALK)
	draw_circle(pos + Vector2(0, -sh), cr, MUSHROOM_CAP)
	draw_circle(pos + Vector2(0, -sh), cr * 0.7, MUSHROOM_CAP * 1.1)
