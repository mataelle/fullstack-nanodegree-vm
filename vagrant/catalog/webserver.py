from flask import Flask, render_template, redirect, request, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

#### json endpoints

@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    return jsonify(items=[i.serialize for i in category.items])

@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(catalog=[c.serialize for c in categories])

#### handlers

@app.route('/category/<int:category_id>')
def CategoryHandler(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    return render_template('category.html', category=category)

@app.route('/category/<int:category_id>/item/<int:item_id>')
def ItemHandler(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('item.html', item=item)

@app.route('/category/<int:category_id>/item/new', methods = ['GET', 'POST'])
def NewItemHandler(category_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id = category_id).one()
        return render_template('item_new.html',
                               category = category)

    else:
        name = request.form.get('item_name', None)
        description = request.form.get('description', None)
        category = session.query(Category).filter_by(id = category_id).one()
        if not name or not description:
           return render_template('item_new.html',
                                  category = category,
                                  name = name,
                                  description = description,
                                  err_msg = True)
        item = Item(name = name, description = description, category=category)
        session.add(item)
        session.commit()
        return redirect(url_for('ItemHandler', category_id = category_id, item_id = item.id))

@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def EditItemHandler(category_id, item_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id = category_id).one()
        item = session.query(Item).filter_by(id = item_id).one()
        return render_template('item_edit.html',
                               item_id = item_id,
                               category = category,
                               name = item.name,
                               description = item.description)
    else:
        name = request.form.get('item_name', None)
        description = request.form.get('description', None)
        if not name or not description:
           return render_template('item_edit.html',
                                  item_id = item_id,
                                  name = name,
                                  description = description,
                                  err_msg = True)
        category = session.query(Category).filter_by(id = category_id).one()
        item = session.query(Item).filter_by(id = item_id).one()
        item.name = name
        item.description = description
        session.add(item)
        session.commit()
        return render_template('item.html', category=category, item=item)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def DeleteItemHandler(category_id, item_id):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id = category_id).one()
        return render_template('item_delete.html',
                                category=category,
                                item_id = item_id)
    else:
        category = session.query(Category).filter_by(id = category_id).one()
        item = session.query(Item).filter_by(id = item_id).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('CategoryHandler', category_id = category_id))

@app.route('/category')
@app.route('/')
def MainHandler():
    categories = session.query(Category).all()
    latest_items = session.query(Item).order_by('created').limit(10)
    return render_template('front.html', categories=categories, latest_items=latest_items)

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)