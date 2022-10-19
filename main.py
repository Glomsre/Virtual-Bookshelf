from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name_collection_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#CREATE TABLE
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f'<Books {self.title}>'

db.create_all()

@app.route('/')
def home():
    all_books = Books.query.all()
    return render_template('index.html', books_db=all_books)

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/receive_data", methods=['GET', 'POST'])
def receive_data():
    title = request.form['bookname']
    author = request.form['bookauthor']
    rating = request.form['rating']
    if title != "" and author != "" and rating is not None:
    # CREATE RECORD
        new_book = Books(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/')

    return render_template('add.html')

@app.route('/edit_rating', methods=["GET", "POST"])
def edit_rating():
    if request.method == "POST":
        # UPDATE RECORD
        book_id = request.form['id']
        book_to_update = Books.query.get(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect('/')
    book_id = request.args.get('id')
    book_selected = Books.query.get(book_id)
    return render_template('edit_rating.html', book=book_selected)


@app.route('/delete_record')
def delete_record():
    # DELETE RECORD BY ID
    book_id = request.args.get('id')
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

