from flask import Flask, request, redirect, url_for, render_template_string
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


@app.route('/', methods=['GET', 'POST'])
def list():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT id, first_name, last_name FROM names;')
    names = cur.fetchall()
    cur.close()
    conn.close()
    
    html = '<html><body><ul>'
    for name in names:
        # Include a link with an X button for each record
        html += f'<li>{name[0]} {name[1]} {name[2]} - <a href="/delete/{name[0]}">X</a></li>'
    html += '</ul></body></html>'
    return html

@app.route('/delete/<int:id>')
def delete(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('DELETE FROM names WHERE id = %s;', (id,))  # Delete the record by ID
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('remaining'))  # Redirect to the remaining route

@app.route('/remaining')
def remaining():
    
    conn = psycopg2.connect(DATABASE_URL)
    cur2 = conn.cursor()
    cur2.execute('SELECT COUNT(*) FROM names;')
    total_count = cur2.fetchall()
    cur2.close()
    conn.close()
    
    html = '<html><body>'

    html += f'Total count: {total_count[0][0]}'
    html += '<br>'
    html += '<a href="/">Go back to list</a>'
    html += '</body></html>'

    return html
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

