import os
import pickle
import numpy as np
from deepface import DeepFace

DATA_DIR = "backend/face/data/mohit"
OUT_FILE = "backend/face/embeddings/mohit.pkl"

print("🔄 Training face embeddings...")

embeddings = []

for img_name in sorted(os.listdir(DATA_DIR)):
    img_path = os.path.join(DATA_DIR, img_name)

    try:
        reps = DeepFace.represent(
            img_path=img_path,
            model_name="ArcFace",
            detector_backend="opencv",
            enforce_detection=True
        )

        if not reps:
            print(f"⚠️ No face in {img_name}")
            continue

        emb = np.array(reps[0]["embedding"], dtype=np.float32)
        emb /= np.linalg.norm(emb)

        embeddings.append(emb)
        print(f"✅ Processed {img_name}")

    except Exception as e:
        print(f"❌ Skipped {img_name}: {e}")

if len(embeddings) == 0:
    raise RuntimeError("❌ No valid faces found. Training failed.")

# Mean embedding
mean_embedding = np.mean(embeddings, axis=0)
mean_embedding /= np.linalg.norm(mean_embedding)

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

with open(OUT_FILE, "wb") as f:
    pickle.dump(mean_embedding, f)

print("🎉 Training complete")
print("📁 Saved →", OUT_FILE)
print("📸 Faces used →", len(embeddings))
