from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/category/<int:category_id>')
def CategoryHandler(category_id):
    return "Here will be category with list of items"

@app.route('/category/<int:category_id>/item/<int:item_id>')
def ItemHandler(category_id, item_id):
    return "item"

@app.route('/category/<int:category_id>/item/new')
def NewItemHandler(category_id):
    return "new item"

@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def EditItemHandler(category_id, item_id):
    return "edit item"

@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def DeleteItemHandler(category_id, item_id):
    return "delete item"

@app.route('/category')
@app.route('/')
def MainHandler():
    return "Main"

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)