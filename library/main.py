from flask import Flask, render_template, request, redirect, url_for,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,Float,Integer

# creating database
class Base(DeclarativeBase):
    pass
    #we can add feauture
# create the extension
db=SQLAlchemy(model_class=Base)
# creating flask server
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///dummy.db"
# intialise the app with extension
db.init_app(app)
# creating table
class Book(db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True,unique=True)
    rating:Mapped[float] = mapped_column(Float, nullable=False)
    title:Mapped[str]=mapped_column(String(250),unique=True,nullable=False)
    author:Mapped[str]=mapped_column(String(250),unique=False,nullable=False)
# create table scheme in data base require app context
with app.app_context():
    db.create_all()

#home page
@app.route('/')
def home():
    # read the data from database
    with app.app_context():
        books = db.session.execute(db.select(Book)).scalars()
        all_books = []
        # adding books in database to list
        for i in books:
            dummy = {}
            dummy["id"] = i.id
            dummy["title"] = i.title
            dummy["author"] = i.author
            dummy["rating"] = i.rating
            all_books.append(dummy)
    data=all_books
    response=make_response(render_template("welcome.html",d=data))
    response.headers['cache-control']='no-state,no-cache,must-revalidate,post-check=0,pre-check=0,max-age=0'
    response.headers['Pragma']='no-cache'
    response.headers['Expires']='0'
    return response


@app.route("/add",methods=["POST","GET"])
def add():
    if request.method=="POST":
        # add new book to database


        newbook=Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"],
        )
        db.session.add(newbook)
        db.session.commit()


        return redirect(url_for("home")) #redirect to url
    return render_template("index.html")

# edit rating option
@app.route("/edit",methods=["POST","GET"])
def edit():
    id=request.args.get("id")

    book_to_edit = db.session.execute(db.select(Book).where(Book.id == id)).scalar()



    if request.method=="POST":

        # editing database(update)

        book_to_edit.rating=request.form["newrating"]
        db.session.commit()
        # updated data

        return redirect(url_for("home"))


    return render_template("edit.html",data=book_to_edit)
# adding delete option
@app.route("/delete")

def delete():
    id=request.args.get("id")
    print(id)
    # delete book from database
    book_to_delete=db.session.execute(db.select(Book).where(Book.id==id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
