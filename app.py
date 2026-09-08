from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

DB = "database.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_conn()
    contactos = conn.execute("SELECT * FROM contactos").fetchall()
    conn.close()
    return render_template("index.html", contactos=contactos)

@app.route("/buscar", methods=["GET"])
def buscar():
    nombre = request.args.get("nombre", "")
    conn = get_conn()
    contactos = conn.execute(
        "SELECT * FROM contactos WHERE nombre LIKE ?", ("%" + nombre + "%",)
    ).fetchall()
    conn.close()
    return render_template("index.html", contactos=contactos)


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        conn = get_conn()
        conn.execute(
            "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)",
            (nombre, telefono, email),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("agregar.html")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_conn()
    conn.execute("DELETE FROM contactos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)