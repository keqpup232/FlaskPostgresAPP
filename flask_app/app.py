import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host=os.environ['HOST_ENV'],
                            database=os.environ['POSTGRES_DB'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD']
                            )
    return conn


@app.route('/', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        if request.form['name'] == '' or request.form['email'] == '':
            return render_template('index.html', error_exists='none', error_null='flex')
        else:
            name = request.form['name']
            email = request.form['email']
        if request.form['db_test'] == 'test':
            db_conf = request.form['db_conf']
            conn = psycopg2.connect(db_conf)
        else:
            conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO users (name, email)'
                        'VALUES (%s, %s)',
                        (name, email))
        except psycopg2.errors.UniqueViolation as e:
            conn.rollback()
            return render_template('index.html', error_exists='flex', error_null='none')
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('last5users'))
    return render_template('index.html', error_exists='none', error_null='none')


@app.route('/last5users/')
def last5users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users ORDER BY record_date DESC LIMIT 5;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('users.html', users=users)


@app.route('/allbooks/')
def allbooks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('allbooks.html', books=books)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('allbooks'))

    return render_template('create.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)