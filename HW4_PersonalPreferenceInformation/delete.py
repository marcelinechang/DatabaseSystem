from flask import Blueprint, redirect, url_for
from bson.objectid import ObjectId, InvalidId
from config import collection

delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/delete/<id>', methods=['POST'])
def delete(id):
    print(f"Received raw ID: {id}")
    try:
        obj_id = ObjectId(id)
        print(f"Converted ObjectId: {obj_id}")
        collection.delete_one({"_id": obj_id})
        return redirect(url_for('index'))
    except InvalidId:
        print("Invalid ObjectId format!")
        return "Invalid ID", 400
    except Exception as e:
        print(f"Error occurred: {e}")
        return str(e), 400
