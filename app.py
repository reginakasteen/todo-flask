from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap

data = [
    {
        "id": 1,
        "title": "Buy groceries",
        "completed": False
    },
    {
        "id": 2,
        "title": "Finish homework",
        "completed": True
    },
    {
        "id": 3,
        "title": "Clean the house",
        "completed": False
    },
    {
        "id": 4,
        "title": "Walk the dog",
        "completed": True
    },
    {
        "id": 5,
        "title": "Read a book",
        "completed": False
    }
]

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="new_key")
Bootstrap(app)

@app.route('/')
def home():
    tasks_completed = all(todo["completed"] for todo in data)
    return render_template("base.html", todo_list = data, tasks_completed=tasks_completed)

def get_last_id():
    if len(data) > 0:
        return max(todo["id"] for todo in data) + 1
    else:
        return 1

@app.route('/add', methods=["POST"])
def create_todo():
    title = request.form.get("title", "").strip()
    if title:
        data.append({
            'id': get_last_id(),
            'title': title,
            'completed': False,
        })
    else:
        flash('Title of the task can not be empty', 'error')
    return redirect(url_for("home"))

@app.route('/update/<int:id>')
def update_todo(id):
    for todo in data:
        if todo["id"] == id:
            todo["completed"] = not todo["completed"]
    else:
        flash('No task found', 'error')
    return redirect(url_for("home"))


@app.route('/delete/<int:id>')
def delete_todo(id):
    for todo in data:
        if todo["id"] == id:
            data.remove(todo)
    else:
        flash('No task found', 'error')
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)