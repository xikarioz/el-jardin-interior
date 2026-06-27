# ProgressionManager — Controla el avance por capítulos
#
# 10 capítulos, cada uno con:
#   - bioma (zona del jardín)
#   - animal guía
#   - tests camuflados (ids)
#   - páginas de diálogo desde archivos .md
#
# Señales:
#   chapter_changed(chapter: int)
#   page_changed(page: int, text: String, animal: String)

extends Node

var current_chapter: int = 0
var current_page: int = 0
var total_chapters: int = 10
var unlocked_chapters: Array = [true, false, false, false, false, false, false, false, false, false]
var chapter_pages: Array = []  # [chapter][page] = {"text": "...", "animal": "...", "mechanic": "..."}

signal chapter_changed(chapter: int, name: String)
signal page_shown(page: int, text: String, animal: String)
signal chapter_completed(chapter: int)

func _ready():
	_load_chapter_data()

func _load_chapter_data():
	var dialogos_dir = "res://assets/data/dialogos/"
	
	for ch_idx in range(total_chapters):
		var path = dialogos_dir + "capitulo_%02d.json" % (ch_idx + 1)
		var file = FileAccess.open(path, FileAccess.READ)
		if file:
			var data = JSON.parse_string(file.get_as_text())
			chapter_pages.append(data if data is Array else [])
		else:
			push_warning("Dialogos JSON not found: ", path)
			chapter_pages.append([])

func _detect_animal(text: String) -> String:
	var lower = text.to_lower()
	if lower.contains("tortuga"): return "tortuga"
	if lower.contains("zorro"): return "zorro"
	if lower.contains("búho") or lower.contains("buho"): return "buho"
	if lower.contains("mariposa"): return "mariposa"
	if lower.contains("caracol"): return "caracol"
	if lower.contains("pájaro") or lower.contains("pajaro"): return "pajaro"
	return ""

func _detect_mechanic(text: String) -> String:
	var lower = text.to_lower()
	if lower.contains("flores que cambian"): return "stroop"
	if lower.contains("flechas"): return "flanker"
	if lower.contains("estrella") or lower.contains("aparece"): return "cpt"
	if lower.contains("luciérnaga") or lower.contains("secuencia"): return "corsi"
	if lower.contains("números") or lower.contains("sonidos"): return "span"
	if lower.contains("regla cambia") or lower.contains("clasificar"): return "wcst"
	if lower.contains("palabra") or lower.contains("rima"): return "lenguaje"
	if lower.contains("número") or lower.contains("suma"): return "matematicas"
	if lower.contains("espejo") or lower.contains("girar"): return "visuoespacial"
	if lower.contains("rápido") or lower.contains("ritmo"): return "velocidad"
	if lower.contains("emoción") or lower.contains("flor triste"): return "socioemocional"
	return ""

func start_chapter(chapter: int) -> bool:
	if chapter < 0 or chapter >= total_chapters:
		return false
	if not unlocked_chapters[chapter]:
		return false
	
	current_chapter = chapter
	current_page = 0
	chapter_changed.emit(chapter, _get_chapter_name(chapter))
	return true

func show_next_page() -> bool:
	if current_chapter >= chapter_pages.size():
		return false
	var pages = chapter_pages[current_chapter]
	if current_page >= pages.size():
		return false
	
	var page_data = pages[current_page]
	page_shown.emit(current_page, page_data.text, page_data.animal)
	current_page += 1
	
	if current_page >= pages.size():
		chapter_completed.emit(current_chapter)
		if current_chapter + 1 < total_chapters:
			unlocked_chapters[current_chapter + 1] = true
	
	return true

func get_current_page_data() -> Dictionary:
	if current_chapter < chapter_pages.size() and current_page < chapter_pages[current_chapter].size():
		return chapter_pages[current_chapter][current_page]
	return {"text": "", "animal": "", "mechanic": ""}

func _get_chapter_name(chapter: int) -> String:
	var names = [
		"El Despertar", "El Bosque que Cambia", "El Río de los Recuerdos",
		"La Montaña de las Decisiones", "El Valle de las Palabras", "La Torre de los Números",
		"La Gruta de los Espejos", "El Camino del Viento", "El Espejo", "El Florecimiento"
	]
	return names[chapter] if chapter < names.size() else ""

func get_chapter_progress() -> float:
	if chapter_pages.size() <= current_chapter:
		return 1.0
	var total = chapter_pages[current_chapter].size()
	return float(current_page) / float(total) if total > 0 else 1.0

func save_state() -> Dictionary:
	return {
		"current_chapter": current_chapter,
		"current_page": current_page,
		"unlocked_chapters": unlocked_chapters
	}

func load_state(data: Dictionary):
	if data.has("current_chapter"): current_chapter = data.current_chapter
	if data.has("current_page"): current_page = data.current_page
	if data.has("unlocked_chapters"): unlocked_chapters = data.unlocked_chapters
