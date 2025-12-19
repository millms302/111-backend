from flask import Flask, jsonify, request
import sqlite3



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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)