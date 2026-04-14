from flask import Flask, render_template, request, redirect, url_for
from database import get_db

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()

    if request.method == "POST":
        note_text = request.form.get("note")
        if note_text:
            conn.execute("INSERT INTO notes (content) VALUES (?)", (note_text,))
            conn.commit()
        return redirect(url_for("index"))

    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return render_template("index.html", notes=notes)


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

