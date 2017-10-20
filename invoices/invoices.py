from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, make_response
import os
import sqlite3
import json



app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'invoices.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('INVOICES_SETTINGS', silent=True)





def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

#Init database from cmd when installing
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#login - not yet used
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            #return redirect(url_for('show_entries'))
    return 0
    #return render_template('login.html', error=error)

#logout - not yet used
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


#return errors in json format
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#GET - retrieve all invoices
@app.route('/invoices')
def get_invoices():
    db = get_db()
    cur = db.execute('select id, customer, total from invoices order by id desc')
    entries = cur.fetchall()
    rows = [ dict(entrie) for entrie in entries ]
    json_data = json.dumps(rows)
    return json_data
    #return jsonify({'invoices':entries})

#GET - retrieve one invoice
@app.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    db = get_db()
    cur = db.execute('SELECT id, customer, total FROM invoices WHERE id='+str(invoice_id))
    entries = cur.fetchall()
    if len(entries) == 0:
        abort(404)
    rows = [ dict(entrie) for entrie in entries ]
    json_data = json.dumps(rows)
    return json_data
    #return jsonify({'invoice': entries[0]})

#POST - insert new invoice
@app.route('/invoices', methods=['POST'])
def create_invoice():
    #if not session.get('logged_in'):
    #    abort(401)
    if not request.json or not 'customer' in request.json:
        abort(400)
    db = get_db()
    db.execute('insert into invoices (customer, total) values (?, ?)',
                 [request.json['customer'], request.json['total']])
    db.commit()
    #return last inserted as a response
    cur = db.execute('SELECT * FROM invoices WHERE id=last_insert_rowid()')
    entries = cur.fetchall()
    if len(entries) == 0:
        abort(404)
    rows = [ dict(entrie) for entrie in entries ]
    json_data = json.dumps(rows)
    return json_data, 201

#PUT - updates invoice
@app.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    #check if record exists
    db = get_db()
    cur = db.execute('SELECT count(*) FROM invoices WHERE id='+str(invoice_id))
    count = cur.fetchone()[0]
    #check for correct parameters
    if cur == 0:
        abort(404)
    if not request.json:
        abort(400)
    if not 'customer' in request.json:
        abort(400)
    if not 'total' in request.json:
        abort(400)
    #update
    db.execute('UPDATE invoices SET '
               'customer="' + request.json['customer']
               + '", total='+ str(request.json['total'])
               + ' WHERE id=' + str(invoice_id))
    db.commit()
    #return updated record
    db = get_db()
    cur = db.execute('SELECT id, customer, total FROM invoices WHERE id='+str(invoice_id))
    entries = cur.fetchall()
    if len(entries) == 0:
        abort(404)
    rows = [ dict(entrie) for entrie in entries ]
    json_data = json.dumps(rows)
    return json_data

#DELETE - deletes an invoice
@app.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    db = get_db()
    cur = db.execute('DELETE FROM invoices WHERE id=?',(str(invoice_id),))
    db.commit()
    return jsonify({'result': True})



