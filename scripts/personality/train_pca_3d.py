"""
Train PCA: 17-dim personality → 3D latent space
Generates: pca_3d.onnx + pca_3d_mean.npy + pca_3d_components.npy
"""

import numpy as np
from sklearn.decomposition import PCA

np.random.seed(42)

# Synthetic dataset: 5000 profiles with realistic correlations
n = 5000

# Big Five (correlated)
o = np.random.normal(50, 20, n)  # openness
c = np.random.normal(50, 20, n)  # conscientiousness  
e = np.random.normal(50, 20, n)  # extraversion
a = np.random.normal(50, 20, n)  # agreeableness
n_dim = np.random.normal(50, 20, n)  # neuroticism

# Cognitive (correlated with Big Five)
atencion = c * 0.3 + np.random.normal(35, 15, n)
inhibicion = c * 0.4 + np.random.normal(30, 15, n)
mem_verbal = o * 0.3 + np.random.normal(35, 15, n)
mem_viso = o * 0.2 + np.random.normal(40, 15, n)
flex_cog = o * 0.4 + np.random.normal(30, 15, n)
razon = o * 0.3 + c * 0.2 + np.random.normal(25, 15, n)
velocidad = e * 0.2 + np.random.normal(40, 15, n)
cog_social = a * 0.4 + np.random.normal(30, 15, n)

# Composite
estilo_ap = o * 0.3 - c * 0.2 + np.random.normal(50, 10, n)  # holístico vs secuencial
tol_frust = c * 0.3 - n_dim * 0.3 + np.random.normal(50, 10, n)
impulsiv = e * 0.2 - c * 0.3 + np.random.normal(50, 10, n)
creatividad = o * 0.5 + np.random.normal(25, 15, n)

X = np.column_stack([
    o, c, e, a, n_dim,
    atencion, inhibicion, mem_verbal, mem_viso,
    flex_cog, razon, velocidad, cog_social,
    estilo_ap, tol_frust, impulsiv, creatividad
])

X = np.clip(X, 0, 100)

pca = PCA(n_components=3, whiten=False)
X_3d = pca.fit_transform(X)

var_explained = pca.explained_variance_ratio_
print(f"Varianza explicada: {var_explained}")
print(f"Varianza total 3D: {sum(var_explained):.3f}")

# Export
np.save("pca_3d_mean.npy", pca.mean_)
np.save("pca_3d_components.npy", pca.components_)

# Also save as text for Godot (no numpy needed)
mean_list = pca.mean_.tolist()
components_list = pca.components_.tolist()

import json, os
with open("pca_3d_data.json", "w") as f:
    json.dump({"mean": mean_list, "components": components_list}, f)

print(f"Shape components: {pca.components_.shape}")  # (3, 17)
print("✅ PCA exportado")

# Print component interpretation
for i, comp in enumerate(pca.components_):
    top_idx = np.argsort(np.abs(comp))[-3:]
    print(f"  PC{i+1}: dims {top_idx.tolist()} con pesos {comp[top_idx].round(3)}")

# Project 351 characters
print("\n--- Proyectando 351 personajes ---")
with open(os.path.expanduser("~/el-jardin-interior/data/character-database.json")) as f:
    chars = json.load(f)

# For each character, build 17-dim vector from their personality + cognitive traits
char_3d = []
for ch in chars:
    p = ch.get("personality", {})
    # Align: [o, c, e, a, n, atencion, inhibicion, ...]
    vec_17 = np.array([
        p.get("openness", 50), p.get("conscientiousness", 50),
        p.get("extraversion", 50), p.get("agreeableness", 50),
        p.get("neuroticism", 50),
        # cognitive traits approximated from personality or use defaults
        p.get("openness", 50) * 0.7 + 15,  # atencion proxy
        p.get("conscientiousness", 50) * 0.7 + 15,
        p.get("openness", 50) * 0.6 + 20,
        p.get("openness", 50) * 0.5 + 25,
        p.get("openness", 50) * 0.6 + 20,
        p.get("openness", 50) * 0.5 + p.get("conscientiousness", 50) * 0.3 + 10,
        p.get("extraversion", 50) * 0.5 + 25,
        p.get("agreeableness", 50) * 0.6 + 20,
        50, 50, 50, p.get("openness", 50) * 0.7 + 15
    ])
    vec_17 = np.clip(vec_17, 0, 100)
    vec_3d = pca.transform(vec_17.reshape(1, -1))[0]
    ch["latent_3d"] = vec_3d.tolist()
    char_3d.append(ch)

with open("character-database-3d.json", "w") as f:
    json.dump(char_3d, f, indent=2)

print(f"✅ {len(char_3d)} personajes proyectados a 3D")
print("Archivos generados: pca_3d_data.json, pca_3d_mean.npy, pca_3d_components.npy, character-database-3d.json")
