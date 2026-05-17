from flask import Flask, redirect, request, session, render_template
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = "12345"

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "password":
            session["logged_in"] = True
            return redirect("/books")
        else:
            return render_template(
                "login.html",
                error = "Login Failed",
            )
    return render_template("login.html")

@app.route("/books", methods=["GET", "POST"])
def books():
    if "logged_in" not in session:
        return redirect("/login")
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    error = ""

    if request.method == "POST":
        isbn = request.form["isbn"].strip()
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key=AIzaSyA0wd2QZFr4TkN5iawyanmD2gIL_0Fdons"
        response = requests.get(url)
        data = response.json()



        if "items" in data:
            book = data["items"][0]["volumeInfo"]
            title = book.get("title", "Unknown")
            author = book.get("authors", ["Unknown"])[0]
            page = book.get("pageCount", 0)
            rating = book.get("averageRating", 0)

            cursor.execute("""
                INSERT INTO books (isbn, title, author, pages, rating)
                VALUES (?, ?, ?, ?, ?)""", (isbn, title, author, page, rating))
            conn.commit()
        else:
            error = "No books found"

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template("books.html", books=books, error=error)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/books")



if __name__ == '__main__':
    app.run()