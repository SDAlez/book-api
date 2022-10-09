import requests
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'library_admin'
app.config['MYSQL_DATABASE_PASSWORD'] = '1S1!#3iOO#i@'
app.config['MYSQL_DATABASE_DB'] = 'library_database'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/books', methods=['GET', 'POST'])
def books():
    
    if request.method == 'GET':
        
        SQL_QUERY = 'SELECT * FROM books'
        
        cursor.execute(SQL_QUERY)
        book_list = []
        
        for row in cursor:
            
            book = {
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'language': row [3]
            }
            
            book_list.append(book)
            
        return jsonify(book_list), 200
            
    if request.method == 'POST':
        try:
            new_author = request.form['author']
            new_lang = request.form['language']
            new_title = request.form['title']
        except:
            return jsonify('Please, fulfill all information(author, language and title)'), 409
        
        SQL_QUERY = 'INSERT INTO books (`title`, `author`, `language`) VALUES (\'{}\', \'{}\', \'{}\')'
            
        cursor.execute(SQL_QUERY.format(new_title, new_author, new_lang))
        conn.commit()

        return jsonify({'message': 'The book was created successfully'}), 201
    
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    
    
    if request.method == 'GET':
        
        SQL_QUERY = 'SELECT * FROM books WHERE id = {}'
        
        cursor.execute(SQL_QUERY.format(id))
        
        book = {}
        
        for row in cursor:
            
            book = {
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'language': row [3]
            }
            
        return jsonify(book), 200
        
    if request.method == 'DELETE':
        
        SQL_QUERY = 'DELETE FROM books WHERE id = {}'
        
        try:
            cursor.execute(SQL_QUERY.format(id))
            conn.commit()
            
        except:
            return {"message": "The book does not exists"}, 404
        
        return {"message": "The book was deleted successfully"}, 200
        
        
        
    if request.method == 'PUT':
        
        book = requests.get('http://localhost:5000/book/{}'.format(id)).json()
        
        new_author = book['author']
        new_title = book['title']
        new_lang = book['language']
        
        
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
            
        SQL_QUERY = 'UPDATE books SET title = \'{}\', author = \'{}\', language = \'{}\' WHERE id = {}'
            
        try:
            cursor.execute(SQL_QUERY.format(new_title, new_author, new_lang, id))
            
        except:
            return {"message": "The book does not exists"}, 404
        
        conn.commit()
        return jsonify({"message": "The book was altered successfuly"})
            
    
if __name__ == '__main__':
    app.run(debug=True)
        
        
        