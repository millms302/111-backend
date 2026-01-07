from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import date

app = Flask(__name__)

DB_NAME = "budget_manager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME) # opens a connection to the database file named 'budget_manager.db
    cursor = conn.cursor() # Creates a cursor/tool that lets us send commands (SELECT, INSERT,...) to the database

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTs users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT NOT NULL,
        amount INT NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit() # Save changes to the database. This step not needed with 'GET'.
    conn.close() # Close the connection to the database

@app.get("/api/health")
def health_check():
    return jsonify({"status": "OK"}), 200

@app.post("/api/register")
def register():
    data = request.get_json()
    print(data)
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME) # opens a connection to the database file named 'budget_manager.db
    cursor = conn.cursor() # creates a cursor/tool that lets us send commands to the database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) # Executes an SQL statement..
    conn.commit()
    conn.close()

    
    return jsonify({"message": "user registered successfully"}), 201

@app.get("/api/users")
def get_users():
    conn=sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows columns values to be retrieved by name, row ["username"]
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users")
    rows = cursor.fetchall() # retrieves all rows from the result of the query.
    print(rows)
    conn.close()

    users=[]
    for row in rows:
        user= {"id": row["id"], "username": row["username"]}
        users.append(user)

    return jsonify({
        "success": True,
        "message":"Users Retrieved Successfully",
        "data": users
        }), 200

@app.get("/api/users/<int:user_id>")
def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    # Validate if user exists
    cursor.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
    if not row.fetchone(): #retrieves a single row from the result.
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    conn.close()

    return jsonify({
        "success": True,
        "message": "User retrieved successfully",
        "data":{"id": row["id"], "username": row["username"]}
    }), 200

@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Validate if user exists
    cursor.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
    if not cursor.fetchone(): #retrieves a single row from the result.
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


    return jsonify({
        "success": True,
        "message": "User Deleted Successfully"
    }), 200

@app.put("/api/users/<int:user_id>")
def update_user(user_id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (username,password, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "user updated successfully"
    }), 200

#-----------------Expenses----------------------

@app.post("/api/expenses")
def create_expense():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    amount = data.get("amount")
    date_str = date.today()
    category = data.get("category")
    user_id = data.get("user_id")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (title, description, amount, date, category, user_id) 
        VALUES (?,?,?,?,?,?)
    """, (title, description, amount, date_str, category, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Expense created successfully."
    }), 201
#SESSION 3

# Frontend 
@app.get("/")
def home():
    return render_template("home.html")


@app.get("/about") 
def about():
    my_name = "Mike"
    hobbies = ["Guitar", "Skateboarding", "Gaming", "Lego", "Staring Contests"]
    return render_template("about.html", name=my_name, hobbies=hobbies)

@app.get("/contact")
def contact():
    contact_info = {
        "Email": "crazymike@cmst.com",
        "Phone": "314-867-5309",
        "Address": "123 Music Street, Saint Louis, MO 63125"
    }
    
    return render_template("contact.html", contact_info=contact_info)

@app.get("/login")
def login():
    return render_template("login.html")






if __name__ == "__main__":
    init_db()
    app.run(debug=True, )