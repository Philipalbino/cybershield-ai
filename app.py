import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from ai_engine import analyze_message  # Your AI engine

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "super-secret-dev-key-123"

# ===============================
# DATABASE INITIALIZATION
# ===============================
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

# ===============================
# ROUTES
# ===============================

@app.route("/")
def home():
    return render_template("index.html")

# -------------------------------
# REGISTER
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already exists")
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# -------------------------------
# LOGIN
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username=?", (username,))
        row = c.fetchone()
        conn.close()

        if row and check_password_hash(row[1], password):
            session["user_id"] = row[0]
            session["username"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# -------------------------------
# LOGOUT
# -------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------------------------------
# DASHBOARD
# -------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session["username"])

# -------------------------------
# CHAT
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Default conversation (single conversation per user)
    c.execute("SELECT id FROM conversations WHERE user_id=?", (session["user_id"],))
    row = c.fetchone()
    if row:
        conversation_id = row[0]
    else:
        c.execute("INSERT INTO conversations (user_id, title) VALUES (?, ?)",
                  (session["user_id"], "Main Conversation"))
        conn.commit()
        conversation_id = c.lastrowid

    # 1️⃣ Save user message
    c.execute(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        (conversation_id, "user", user_input)
    )
    conn.commit()

    # 2️⃣ Get AI response
    ai_response = analyze_message(user_input)

    # 3️⃣ Save AI response
    c.execute(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        (conversation_id, "assistant", ai_response)
    )
    conn.commit()

    # 4️⃣ Fetch full conversation history
    c.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC",
        (conversation_id,)
    )
    messages = c.fetchall()
    conn.close()

    return jsonify({"messages": messages})

# -------------------------------
# GET MESSAGES
# -------------------------------
# app.py

@app.route("/get_messages", methods=["GET"])
def get_messages():
    """Return all messages for the default conversation for the logged-in user."""
    if "user_id" not in session:
        return jsonify([])

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Get default conversation for the user
    c.execute("""
        SELECT id FROM conversations
        WHERE user_id = ?
        ORDER BY created_at ASC
        LIMIT 1
    """, (session["user_id"],))
    row = c.fetchone()

    if not row:
        # If no conversation exists, create one
        c.execute("INSERT INTO conversations (user_id, title) VALUES (?, ?)", 
                  (session["user_id"], "Main Conversation"))
        conn.commit()
        conversation_id = c.lastrowid
    else:
        conversation_id = row[0]

    # Fetch all messages for this conversation
    c.execute("""
        SELECT role, content FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
    """, (conversation_id,))
    messages = c.fetchall()
    conn.close()

    return jsonify(messages)

# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
