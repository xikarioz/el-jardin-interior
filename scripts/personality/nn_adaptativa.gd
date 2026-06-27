
const INPUT_SIZE = 10
const HIDDEN_SIZE = 4
const OUTPUT_SIZE = 1

var w_ih: Array  # [INPUT_SIZE][HIDDEN_SIZE]
var b_h: Array   # [HIDDEN_SIZE]
var w_ho: Array  # [HIDDEN_SIZE][OUTPUT_SIZE]
var b_o: Array   # [OUTPUT_SIZE]

var learning_rate = 0.01
var momentum = 0.9

var _v_w_ih: Array
var _v_b_h: Array
var _v_w_ho: Array
var _v_b_o: Array

func _init() -> void:
	_randomize_weights()

func _randomize_weights() -> void:
	w_ih = _rand_mat(INPUT_SIZE, HIDDEN_SIZE, 0.1)
	b_h = _rand_vec(HIDDEN_SIZE, 0.0)
	w_ho = _rand_mat(HIDDEN_SIZE, OUTPUT_SIZE, 0.1)
	b_o = _rand_vec(OUTPUT_SIZE, 0.0)

	_v_w_ih = _zeros_mat(INPUT_SIZE, HIDDEN_SIZE)
	_v_b_h = _zeros_vec(HIDDEN_SIZE)
	_v_w_ho = _zeros_mat(HIDDEN_SIZE, OUTPUT_SIZE)
	_v_b_o = _zeros_vec(OUTPUT_SIZE)

func _rand_mat(rows: int, cols: int, scale: float) -> Array:
	var m: Array = []
	m.resize(rows)
	for i in rows:
		m[i] = _rand_vec(cols, scale)
	return m

func _rand_vec(size: int, scale: float) -> Array:
	var v: Array = []
	v.resize(size)
	for i in size:
		v[i] = randf_range(-scale, scale)
	return v

func _zeros_mat(rows: int, cols: int) -> Array:
	var m: Array = []
	m.resize(rows)
	for i in rows:
		m[i] = _zeros_vec(cols)
	return m

func _zeros_vec(size: int) -> Array:
	var v: Array = []
	v.resize(size)
	for i in size:
		v[i] = 0.0
	return v

func _relu(x: float) -> float:
	return max(0.0, x)

func _relu_deriv(x: float) -> float:
	return 1.0 if x > 0.0 else 0.0

func _mat_vec_mul(mat: Array, vec: Array) -> Array:
	var out: Array = []
	out.resize(mat.size())
	for i in mat.size():
		var s = 0.0
		var row = mat[i]
		for j in min(row.size(), vec.size()):
			s += row[j] * vec[j]
		out[i] = s
	return out

func _vec_add(a: Array, b: Array) -> Array:
	var out: Array = []
	out.resize(a.size())
	for i in a.size():
		out[i] = a[i] + b[i]
	return out

func _vec_mul_scalar(v: Array, s: float) -> Array:
	var out: Array = []
	out.resize(v.size())
	for i in v.size():
		out[i] = v[i] * s
	return out

func _outer_vecs(a: Array, b: Array) -> Array:
	var m: Array = []
	m.resize(a.size())
	for i in a.size():
		m[i] = _vec_mul_scalar(b, a[i])
	return m

func _transpose_mat(m: Array) -> Array:
	if m.is_empty():
		return []
	var rows = m.size()
	var cols = m[0].size()
	var t: Array = []
	t.resize(cols)
	for j in cols:
		t[j] = []
		t[j].resize(rows)
		for i in rows:
			t[j][i] = m[i][j]
	return t

func predict(inputs: Array) -> Array:
	if inputs.size() != INPUT_SIZE:
		push_error("NNAdaptativa: input size mismatch (expected ", INPUT_SIZE, ", got ", inputs.size(), ")")
		return [0.0]

	var hidden_pre = _mat_vec_mul(w_ih, inputs)
	var hidden = _vec_add(hidden_pre, b_h)
	for i in hidden.size():
		hidden[i] = _relu(hidden[i])

	var output_pre = _mat_vec_mul(w_ho, hidden)
	var output = _vec_add(output_pre, b_o)

	return output

func forward_full(inputs: Array) -> Dictionary:
	var h_pre = _mat_vec_mul(w_ih, inputs)
	var h = _vec_add(h_pre, b_h)
	for i in h.size():
		h[i] = _relu(h[i])

	var o_pre = _mat_vec_mul(w_ho, h)
	var o = _vec_add(o_pre, b_o)

	return {"hidden": h, "hidden_raw": h_pre, "output": o, "output_raw": o_pre}

func train(inputs: Array, target: float) -> float:
	var f = forward_full(inputs)
	var h = f.hidden
	var h_raw = f.hidden_raw
	var o = f.output

	var error = target - o[0]
	var d_o = error

	var d_h: Array = []
	d_h.resize(HIDDEN_SIZE)
	for i in HIDDEN_SIZE:
		var sum_err = 0.0
		for j in OUTPUT_SIZE:
			sum_err += d_o * w_ho[i][j]
		d_h[i] = sum_err * _relu_deriv(h_raw[i])

	var grad_w_ho = _outer_vecs(d_h, _vec_mul_scalar([d_o], 1.0))
	grad_w_ho = _transpose_mat(grad_w_ho)

	for i in HIDDEN_SIZE:
		for j in OUTPUT_SIZE:
			var delta = learning_rate * d_o * h[i] + momentum * _v_w_ho[i][j]
			w_ho[i][j] += delta
			_v_w_ho[i][j] = delta

	for j in OUTPUT_SIZE:
		var delta = learning_rate * d_o + momentum * _v_b_o[j]
		b_o[j] += delta
		_v_b_o[j] = delta

	var grad_w_ih = _outer_vecs(inputs, d_h)

	for i in INPUT_SIZE:
		for j in HIDDEN_SIZE:
			var delta = learning_rate * d_h[j] * inputs[i] + momentum * _v_w_ih[i][j]
			w_ih[i][j] += delta
			_v_w_ih[i][j] = delta

	for j in HIDDEN_SIZE:
		var delta = learning_rate * d_h[j] + momentum * _v_b_h[j]
		b_h[j] += delta
		_v_b_h[j] = delta

	return abs(error)

func adjust_positive(features: Array) -> float:
	return train(features, 1.0)

func adjust_negative(features: Array) -> float:
	return train(features, -1.0)

func save(path: String) -> void:
	var data = {
		"w_ih": w_ih,
		"b_h": b_h,
		"w_ho": w_ho,
		"b_o": b_o,
		"lr": learning_rate
	}
	var file = FileAccess.open(path, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data))
		file.close()

func load(path: String) -> bool:
	var file = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var json = JSON.new()
	if json.parse(file.get_as_text()) != OK:
		return false
	var data = json.data
	w_ih = data.get("w_ih", w_ih)
	b_h = data.get("b_h", b_h)
	w_ho = data.get("w_ho", w_ho)
	b_o = data.get("b_o", b_o)
	learning_rate = data.get("lr", learning_rate)
	return true
