from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "wdffrfenaia"

app.config["UPLOAD_FOLDER"] = "C:/Users/Shree/PycharmProjects/flask_task_project/static/images"


# Set the path for the database file
db_name = "mydb.db"
db_path = os.path.join(app.root_path, db_name)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        fn = request.form["fullname"]
        em = request.form["email"]
        ps = request.form["password"]

        f = request.files["photo"]
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))



        try:
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute("INSERT INTO student (fullname, email, password, photo) VALUES (?, ?, ?, ?)", (fn, em, ps, f.filename))
            con.commit()
            con.close()
            return redirect(url_for("home"))
        except sqlite3.Error as e:
            print("SQLite error:", e.args[0])
            return "Error: Registration failed. Please try again."
    else:
        return redirect(url_for("home"))

@app.route("/welcome")
def welcome():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM student ORDER BY id DESC")
    data = cur.fetchall()
    con.close()
    return render_template("welcome.html", data=data)

@app.route("/profiles")
def profiles():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    con.close()
    return render_template("profiles.html", data=data)

@app.route("/delete/<email>")
def delete(email):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("DELETE FROM student WHERE email = ?", [email])
    con.commit()
    con.close()
    return redirect(url_for("welcome"))

@app.route("/profile_update/<int:id>", methods=["GET", "POST"])
def profile_update(id):
    if request.method == "POST":
        fn = request.form["fullname"]
        em = request.form["email"]
        ps = request.form["password"]

        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("UPDATE student SET fullname=?, email=?, password=? WHERE id=?", (fn, em, ps, id))
        con.commit()
        con.close()
        return redirect(url_for("welcome"))
    else:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM student WHERE id = ?", [id])
        data = cur.fetchone()
        con.close()
        return render_template("edits.html", data=data)

@app.route("/file_upload")
def file_upload():
    return render_template("file_upload.html")

@app.route("/file_save", methods=["POST"])
def file_save():
    if request.method == "POST":
        f = request.files["photo"]
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
        return "File uploaded successfully"
    else:
        return "Failed"

@app.route("/validate", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        em = request.form["email"]
        ps = request.form["password"]

        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM student WHERE email = ? AND password = ?", (em, ps))
        data = cur.fetchall()

        if len(data) == 1:
            session["username"] = em
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", message="Invalid email or password")
    else:
        return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if session.get("username") is not None:
        username = session.get("username")
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM student WHERE email = ?", [username])
        data = cur.fetchall()
        return render_template("dashboard.html", data=data)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

# Set the database name
db_name = "mydb.db"

# Check if the database file exists, if not, create it
conn = sqlite3.connect(db_name)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS task (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, task_date DATE)")
cur.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, task_date DATE)")
conn.commit()
conn.close()

# Route to insert task data into the database
@app.route("/add_task", methods=["POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form["taskName"]
        task_date = request.form["taskDate"]

        try:
            # Connect to the database
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()

            # Insert task data into the database
            cur.execute("INSERT INTO task (task_name, task_date) VALUES (?, ?)", (task_name, task_date))
            conn.commit()
            conn.close()

            # Redirect to the display tasks page after inserting data
            return redirect(url_for("display_tasks"))
        except sqlite3.Error as e:
            return f"An error occurred: {e}"

# Route to delete task from the database
@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Retrieve task details from the database
        cur.execute("SELECT task_name, task_date FROM task WHERE id = ?", (task_id,))
        task_details = cur.fetchone()

        # Delete task from the task table
        cur.execute("DELETE FROM task WHERE id = ?", (task_id,))

        # Insert deleted task details into history table
        cur.execute("INSERT INTO history (task_name, task_date) VALUES (?, ?)", task_details)

        conn.commit()
        conn.close()

        # Redirect to the display tasks page after deleting task
        return redirect(url_for("display_tasks"))
    except sqlite3.Error as e:
        return f"An error occurred: {e}"

# Route to display task list from the database
@app.route("/display_tasks")
def display_tasks():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Retrieve task data from the database
        cur.execute("SELECT * FROM task")
        tasks = cur.fetchall()

        conn.close()

        # Render the tasks.html template with the retrieved task data
        return render_template("tasks.html", tasks=tasks)
    except sqlite3.Error as e:
        return f"An error occurred: {e}"

# Route to display history of deleted tasks
@app.route("/history")
def history():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Retrieve history data from the database
        cur.execute("SELECT * FROM history")
        history_data = cur.fetchall()

        conn.close()

        # Render the history.html template with the retrieved history data
        return render_template("history.html", history_data=history_data)
    except sqlite3.Error as e:
        return f"An error occurred: {e}"











# Route to display history of deleted tasks and select a date
@app.route("/show_deleted_tasks", methods=["POST"])
def show_deleted_tasks():
    selected_date = request.form.get("historyDate")

    if selected_date:
        try:
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()
            cur.execute("SELECT * FROM history WHERE task_date = ?", (selected_date,))
            deleted_tasks = cur.fetchall()
            conn.close()

            return render_template("record_deleted.html", deleted_tasks=deleted_tasks, selected_date=selected_date)
        except sqlite3.Error as e:
            return f"An error occurred: {e}"
    else:
        return redirect(url_for("dashboard"))







@app.route("/edit_profile/<int:id>", methods=["GET", "POST"])
def edit_profile(id):
    if request.method == "POST":
        fn = request.form["fullname"]
        em = request.form["email"]
        ps = request.form["password"]

        con = sqlite3.connect(db_path)  # Update with your database path
        cur = con.cursor()
        cur.execute("UPDATE student SET fullname=?, email=?, password=? WHERE id=?", (fn, em, ps, id))
        con.commit()
        con.close()
        return redirect(url_for("welcome"))  # Update with your welcome route
    else:
        con = sqlite3.connect(db_path)  # Update with your database path
        cur = con.cursor()
        cur.execute("SELECT * FROM student WHERE id = ?", [id])
        data = cur.fetchone()
        con.close()
        return render_template("edits.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
