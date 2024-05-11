from flask import Flask, request, redirect, url_for, render_template_string
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def setup_database():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS names (
            id SERIAL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            PRIMARY KEY (id)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

HTML_FORM = '''
<html>
  <body>
    <form action="/" method="post">
      First Name: <input type="text" name="first_name"><br>
      Last Name: <input type="text" name="last_name"><br>
      <input type="submit" value="Submit">
    </form>
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def form():
    setup_database()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Check if the entry already exists
        cur.execute('SELECT * FROM names WHERE first_name=%s AND last_name=%s;', (first_name, last_name))
        if cur.fetchone():  # If a result is found, the name pair already exists
            cur.close()
            conn.close()
            return '<html><body><p>Name already exists.</p></body></html>' + HTML_FORM
        else:
            # Insert new entry
            cur.execute('INSERT INTO names (first_name, last_name) VALUES (%s, %s);', (first_name, last_name))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('result'))
    return HTML_FORM

@app.route('/result')
def result():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT first_name, last_name FROM names;')
    names = cur.fetchall()
    cur.close()
    conn.close()

    conn = psycopg2.connect(DATABASE_URL)
    cur2 = conn.cursor()
    cur2.execute('SELECT COUNT(*) FROM names;')
    total_count = cur2.fetchall()
    cur2.close()
    conn.close()
    
    html = '<html><body>'

    html += HTML_FORM

    html += f'Total count: {total_count[0][0]}'
    html += '<br>'

    for name in names:
        html += f'First Name: {name[0]}, Last Name: {name[1]}<br>'
    html += '</body></html>'

    return html
    

if __name__ == '__main__':
    setup_database() 
    app.run(debug=True, host='0.0.0.0')

