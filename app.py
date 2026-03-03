import os
import sqlite3
from flask import Flask, render_template, request, jsonify, session, redirect, Response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from ai_engine import analyze_message

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")


# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


# ================= HOME =================
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return redirect("/dashboard")


# ================= REGISTER =================
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
        except:
            return "Username already exists"

    return render_template("register.html")


# ================= LOGIN =================
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

        return "Invalid credentials"

    return render_template("login.html")

@app.route("/clear")
def clear_chat():
    session.pop("chat_history", None)
    return redirect("/dashboard")



# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ================= CHAT API =================
@app.route("/chat", methods=["POST"])
def chat():
    if "user_id" not in session:
        return jsonify({"reply": "Unauthorized"}), 401

    user_message = request.json["message"]

    # Initialize conversation memory if not exists
    if "chat_history" not in session:
        session["chat_history"] = []

    # Get conversation history
    history = session["chat_history"]

    # Get AI reply with memory
    reply = analyze_message(user_message, history)

    # Update memory
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})

    # Save back to session
    session["chat_history"] = history

    return jsonify({"reply": reply})


# ================= SEO ROUTES =================

@app.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\nAllow: /\nSitemap: https://cybershield-ai-1.onrender.com/sitemap.xml",
        mimetype="text/plain"
    )


@app.route("/sitemap.xml")
def sitemap():
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://cybershield-ai-1.onrender.com/</loc>
      <priority>1.00</priority>
   </url>
   <url>
      <loc>https://cybershield-ai-1.onrender.com/login</loc>
   </url>
   <url>
      <loc>https://cybershield-ai-1.onrender.com/register</loc>
   </url>
</urlset>"""
    return Response(sitemap_xml, mimetype="application/xml")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
