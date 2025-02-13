from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,Float,Integer
# creating database
class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///dummy1.db"
db.init_app(app)
class Book(db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    rating:Mapped[float] = mapped_column(Float, nullable=False)
    title:Mapped[str]=mapped_column(String(250),unique=True,nullable=False)
    author:Mapped[str]=mapped_column(String(250),unique=False,nullable=False)

with app.app_context():
    db.create_all()
#create
#with app.app_context():

    #newbook=Book(title="dumm",author="dumm2", rating=0.1)
    #db.session.add(newbook)
    #db.session.commit()



#update
with app.app_context():
    book=db.session.execute(db.select(Book).where(Book.id==1)).scalar()
    book.title="update"
    db.session.commit()
#delete

with app.app_context():
    book=db.session.execute(db.select(Book).where(Book.id==1)).scalar()
    db.session.delete(book)
    db.session.commit()
#read
with app.app_context():
    book=db.session.execute(db.select(Book).where(Book.id==1)).scalar()
    print(book.title)
