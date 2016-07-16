from flask import Flask, render_template, redirect, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/category/<int:category_id>')
def CategoryHandler(category_id):
    return render_template('category.html', category=None, items=None)

@app.route('/category/<int:category_id>/item/<int:item_id>')
def ItemHandler(category_id, item_id):
    return render_template('item.html', category=None, item=None)

@app.route('/category/<int:category_id>/item/new')
def NewItemHandler(category_id):
    return render_template('item_new.html', category=None, item=None)

@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def EditItemHandler(category_id, item_id):
    return render_template('item_edit.html', category=None, item=None)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def DeleteItemHandler(category_id, item_id):
    return render_template('item_delete.html', category=None, item=None)

@app.route('/category')
@app.route('/')
def MainHandler():
    return render_template('front.html', category=None, latest_items=None)

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)