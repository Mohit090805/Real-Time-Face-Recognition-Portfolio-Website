# backend/app.py

from flask import Flask, request, jsonify, send_from_directory, session, redirect, render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import base64
import pickle
import tempfile
import os
from deepface import DeepFace
from PIL import Image

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Database setup (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/feedback", methods=["POST"])
def feedback():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    new_feedback = Feedback(
        name=name,
        email=email,
        message=message
    )

    db.session.add(new_feedback)
    db.session.commit()

    return redirect(url_for("contact", success="true"))



# =============================
# Load trained face embedding
# =============================
EMB_PATH = "backend/face/embeddings/mohit.pkl" 

with open(EMB_PATH, "rb") as f:
    MOHIT_EMB = pickle.load(f)

MOHIT_EMB = MOHIT_EMB / np.linalg.norm(MOHIT_EMB)

LOCKED_ROUTES = ["/", "/about", "/work", "/contact"]


# =============================
# Route Protection
# =============================
@app.before_request
def protect_routes():
    if request.path.startswith("/api"):
        return

    if (
        request.path in LOCKED_ROUTES
        and not session.get("verified")
        and not request.path.startswith("/security")
        and not request.path.startswith("/static")
    ):
        return redirect("/security")


# =============================
# Pages
# =============================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/work")
def work():
    return render_template("work.html")

@app.route("/contact")
def contact():
    success = request.args.get("success")
    return render_template("contact.html", success=success)

@app.route("/security")
def security():
    return render_template("security.html")

@app.route("/admin")
def admin():
    admin_key = request.args.get("key")
    if admin_key != "admin123":
        abort(403)

    feedbacks = Feedback.query.order_by(Feedback.date.desc()).all()
    return render_template("admin.html", feedbacks=feedbacks)


# =============================
# Face Verification API
# =============================
@app.route("/api/verify-face", methods=["POST"])
def verify_face():
    data = request.json.get("image")
    if not data:
        return jsonify({"success": False, "error": "No image"}), 400

    # Check if it's a full data URL
    if "," in data:
        header, base64_str = data.split(",", 1)
    else:
        base64_str = data

    try:
        img_bytes = base64.b64decode(base64_str)
    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid base64: {e}"}), 400
    
    if not base64_str.strip():
        return jsonify({"success": False, "error": "Empty image"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        f.write(img_bytes)
        temp_path = f.name

    try:
        reps = DeepFace.represent(
            img_path=temp_path,
            model_name="ArcFace",
            detector_backend="opencv",
            enforce_detection=True
        )

        if not reps:
            return jsonify({"success": False, "error": "No face detected"})

        test_emb = np.array(reps[0]["embedding"], dtype=np.float32)
        test_emb /= np.linalg.norm(test_emb)

        similarity = float(np.dot(test_emb, MOHIT_EMB))
        print("🔍 Similarity:", similarity)

        if similarity >= 0.83:
            session["verified"] = True
            return jsonify({"success": True, "similarity": similarity})

        return jsonify({"success": False, "similarity": similarity})

    finally:
        os.remove(temp_path)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
