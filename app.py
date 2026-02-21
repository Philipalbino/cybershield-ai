import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from ai_engine import analyze_message  # Your AI engine
from threading import Thread
import gradio as gr

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

# Initialize DB
init_db()

# ===============================
# GRADIO AI CHATBOT
# ===============================
conversation_history = []

def chat(message):
    conversation_history.append({"role": "user", "content": message})
    reply = analyze_message(conversation_history)
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

iface = gr.Interface(fn=chat, inputs="text", outputs="text", title="CyberShield-AI")

def run_gradio():
    iface.launch(server_name="0.0.0.0", server_port=7860)

Thread(target=run_gradio).start()

# ===============================
# ROUTES
# ===============================
@app.route("/")
def home():
    return render_template("index.html")  # SEO homepage with Google meta tag

@app.route("/robots.txt")
def robots():
    return send_from_directory(".", "robots.txt")

# -----------------------
# Registration
# -----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Username already exists"
    return render_template("register.html")

# -----------------------
# Login
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
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

# -----------------------
# Dashboard
# -----------------------
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

# -----------------------
# Logout
# -----------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -----------------------
# Run Flask
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
