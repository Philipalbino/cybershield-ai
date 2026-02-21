import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from ai_engine import analyze_message  # Your AI engine

load_dotenv()

# ===========================
# Flask app setup
# ===========================
app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("SECRET_KEY") or "super-secret-dev-key-123"

@app.route("/google-site-verification: google701042e23c6c10eb.html")
def google_verify():
    return app.send_static_file("google-site-verification: google701042e23c6c10eb.html")

# ===========================
# Database initialization
# ===========================
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Conversations table
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Messages table
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ===========================
# SEO homepage & static files
# ===========================
@app.route("/")
def home():
    return render_template("index.html")  # Contains Google meta tag

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

# ===========================
# User registration
# ===========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_pw = generate_password_hash(password)

        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Username already exists"

    return render_template("register.html")

# ===========================
# User login
# ===========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# ===========================
# User dashboard
# ===========================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM conversations WHERE user_id=?", (user_id,))
    conversations = c.fetchall()
    conn.close()

    return render_template("dashboard.html", conversations=conversations)

# ===========================
# Logout
# ===========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ===========================
# Chat API endpoint
# ===========================
conversation_history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    conversation_history.append({"role": "user", "content": user_input})
    reply = analyze_message(conversation_history)
    conversation_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

# ===========================
# Production-ready entry
# ===========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
