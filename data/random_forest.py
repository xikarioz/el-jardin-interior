#!/usr/bin/env python3
"""
RandomForestRegressor para personality inference.
Entrena con datos sintéticos, exporta a ONNX.
17 outputs: Big5 (5) + cognitivos (8) + compuestos (4).
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import warnings
warnings.filterwarnings("ignore")

N_PATIENTS = 1000
N_INTERACTIONS = 50
N_FEATURES = 17
N_OUTPUTS = 17
SEED = 42

np.random.seed(SEED)

def _generate_synthetic_patient():
    big5_raw = np.random.normal(0, 1, 5)
    big5 = np.clip(big5_raw, -3, 3)

    cognitivos_raw = np.random.normal(0, 1, 8)
    cognitivos = np.clip(cognitivos_raw, -3, 3)

    compuestos = np.zeros(4)
    compuestos[0] = big5[4] * 0.6 + cognitivos[0] * 0.4
    compuestos[1] = big5[0] * 0.5 + cognitivos[2] * 0.3 + cognitivos[4] * 0.2
    compuestos[2] = cognitivos[1] * 0.5 + cognitivos[3] * 0.3 + big5[2] * 0.2
    compuestos[3] = big5[0] * 0.4 + cognitivos[5] * 0.4 + big5[2] * 0.2

    return np.concatenate([big5, cognitivos, compuestos])

def _interaction_features(patient_vector, t):
    decay = np.exp(-t / N_INTERACTIONS)
    noise = np.random.normal(0, 0.15, N_FEATURES)

    base = patient_vector * decay + noise

    zone_id = np.random.randint(0, 6)
    reaction_time = np.clip(np.random.exponential(1.5), 0.3, 8.0)
    attempts = np.random.randint(1, 8)

    zone_oh = np.zeros(6)
    zone_oh[zone_id] = 1.0

    features = np.concatenate([
        base,
        [reaction_time / 8.0],
        [attempts / 8.0],
        zone_oh
    ])

    return features

N_INPUT_FEATURES = N_FEATURES + 2 + 6

X = np.zeros((N_PATIENTS * N_INTERACTIONS, N_INPUT_FEATURES))
y = np.zeros((N_PATIENTS * N_INTERACTIONS, N_OUTPUTS))

for p in range(N_PATIENTS):
    patient = _generate_synthetic_patient()
    for t in range(N_INTERACTIONS):
        idx = p * N_INTERACTIONS + t
        X[idx] = _interaction_features(patient, t)
        noise = np.random.normal(0, 0.1, N_OUTPUTS)
        y[idx] = patient + noise

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED
)

rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_leaf=4,
    n_jobs=-1,
    random_state=SEED,
    verbose=0
)

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE on test set: {mae:.4f}")

mae_per_output = np.mean(np.abs(y_test - y_pred), axis=0)
output_names = [
    "openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism",
    "memoria", "atencion", "planificacion", "flexibilidad", "inhibicion",
    "velocidad_procesamiento", "toma_decisiones", "razonamiento",
    "comp_emocional", "comp_social", "comp_creativa", "comp_resiliencia"
]
for name, val in zip(output_names, mae_per_output):
    print(f"  MAE {name}: {val:.4f}")

initial_types = [("float_input", FloatTensorType([None, N_INPUT_FEATURES]))]
onx = convert_sklearn(rf, initial_types=initial_types,
                      target_opset=17)

output_path = "/home/francofitte/el-jardin-interior/godot/data/personality_rf.onnx"
with open(output_path, "wb") as f:
    f.write(onx.SerializeToString())
print(f"\nModelo exportado a: {output_path}")
print(f"Input features: {N_INPUT_FEATURES}")
print(f"Output dimensions: {N_OUTPUTS}")
