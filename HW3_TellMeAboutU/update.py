from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId, InvalidId
from config import collection  # Import collection from config.py

update_bp = Blueprint('update', __name__)

@update_bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    try:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            object_id = id 

        if request.method == 'POST':
            update_data = {key: value for key, value in request.form.items() if key != '_id'}
            collection.update_one({"_id": object_id}, {"$set": update_data})
            return redirect(url_for('index'))

        entry = collection.find_one({"_id": object_id})
        if not entry:
            return "Document not found", 404

        entry['_id'] = str(entry['_id']) 
        return render_template('update.html', entry=entry)

    except Exception as e:
        return str(e), 400
