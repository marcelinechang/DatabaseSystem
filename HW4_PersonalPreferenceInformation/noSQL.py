from flask import Flask, render_template, request, redirect, url_for, session
from bson.objectid import ObjectId
from config import collection
from update import update_bp
from delete import delete_bp
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_is_safe_with_me'
app.register_blueprint(update_bp)
app.register_blueprint(delete_bp)

@app.route('/')
def index():
    show_all = session.get('show_all', True)
    data = list(collection.find({})) if show_all else []
    for doc in data:
        doc['_id'] = str(doc['_id'])
    return render_template('index.html', data=data, results=None, show_all=show_all)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        zodiac = request.form.get('zodiac')
        gender = request.form.get('gender')
        song = request.form.get('song')
        color = request.form.get('color')
        lucky_num = request.form.get('lucky_num')
        timestamp = datetime.now()

        new_doc = {'nickname': nickname, 'zodiac': zodiac, 'gender': gender, 'song': song , 'color': color , 'lucky_num':lucky_num, 'created_at': timestamp}
        collection.insert_one(new_doc)

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/search', methods=['POST'])
def search():
    query_text = str(request.form.get("query", ""))
    selected_fields = request.form.getlist('fields') 
    regex_query = {"$regex": query_text, "$options": "i"}
    
    if selected_fields:
        query = {"$or": [{field: regex_query} for field in selected_fields]}
    else:
        query = {"$or": [{field: regex_query} for field in ["nickname", "zodiac", "song", "color", "lucky_num"]]}
    
    data = list(collection.find(query))  
    for doc in data:
        doc['_id'] = str(doc['_id'])

    return render_template('index.html', data=data, search_result=True, show_all=session.get('show_all', False))


@app.route('/show_all', methods=['GET'])
def show_all():
    session['show_all'] = not session.get('show_all', False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
