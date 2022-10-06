import json
from flask import Flask, request, jsonify

app = Flask(__name__)

book_list = [
    {
        "id": 0,
        "author": "Adichie",
        "language": "English",
        "title": "Purple Hibiscus"
    },
    {
        "id": 1,
        "author": "Sun Tzu",
        "language": "Chinese",
        "title": "Art of War"
    },
    {
        "id": 2,
        "author": "Machado de Assis",
        "language": "Portuguese",
        "title": "Don Casmurro"
    }
]

@app.route('/books', methods=['GET', 'POST'])
def books():
    
    
    if request.method == 'GET':
        if(len(book_list) > 0):
            return jsonify(book_list)
        else:
            'Nothing Found', 404
            
            
            
    if request.method == 'POST':
        try:
            new_author = request.form['author']
            new_lang = request.form['language']
            new_title = request.form['title']
            id = len(book_list)
            
            new_obj = {
                'id': id,
                'author': new_author,
                'language': new_lang,
                'title': new_title
            }
            
            book_list.append(new_obj)
            return jsonify(new_obj), 201
        except:
            return jsonify('Please, fulfill all information(author, language and title)'), 409
    
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    
    
    if request.method == 'GET':
        if(len(book_list) > id):
            return jsonify(book_list[id])
        else:
            return "The book does not exists", 404
        
        
        
    if request.method == 'DELETE':
        if(len(book_list) > id):
            book_list.pop(id)
        
            for i in range(len(book_list)):
                book_list[i]['id'] = i
            
            return {"message": "The book was deleted successfully"}, 200
        else:
            return {"message": "The book does not exists"}, 404
        
        
        
    if request.method == 'PUT':
        
        new_author = book_list[id].get('author')
        new_lang = book_list[id].get('language')
        new_title = book_list[id].get('title')
        
        if(len(book_list) > id):        
            try:
                new_author = request.form['author']
            except:
                pass
            
            try:
                new_lang = request.form['language']
            except:
                pass
            
            try: 
                new_title = request.form['title']
            except:
                pass
            
            new_obj = {
                'id': id,
                'author': new_author,
                'language': new_lang,
                'title': new_title
            }
            
            book_list[id] = new_obj
            
            return jsonify(new_obj)
            
        else:
            return {"message": "The book does not exists"}, 404
            
    
if __name__ == '__main__':
    app.run(debug=True)
        
        
        