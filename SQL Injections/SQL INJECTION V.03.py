from flask import Flask, render_template_string, request
import mysql.connector

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="lab_db"
        )

        cursor = db.cursor(dictionary=True)

        # Vulnerable SQL query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        cursor.execute(query)
        users = cursor.fetchall()

        if users:
            message = "Access Granted!"
        else:
            message = "Access Denied!"

        cursor.close()
        db.close()

    return render_template_string('''
        <h2>SQL Injection Lab</h2>
        <form method="POST">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
        <p>{{ message }}</p>
    ''', message=message)

if __name__ == '__main__':
    app.run(debug=False)