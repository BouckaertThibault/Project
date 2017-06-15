from flask import Flask
from flask import flash, redirect, render_template, request, session, abort
import os
import pygal
from DbClass import DbClass


app = Flask(__name__)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin12345' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route('/temperatuur')
def temperatuur():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        graph = pygal.Line()
        graph.title = 'Gemeten temperatuur'
        graph.x_labels = DbClass.getDatum(DbClass())
        graph.add('Temperatuur', DbClass.getTemperatuur(DbClass()))
        graph_data = graph.render_data_uri()
        return render_template('temperatuur.html', graph_data=graph_data)




@app.route('/reservoir')
def reservoir():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        graph = pygal.Line()
        graph.title = 'Aantal liter in reservoir'
        graph.x_labels = DbClass.getDatum(DbClass())
        graph.add('Reservoir', DbClass.getTemperatuur(DbClass()))
        graph_data = graph.render_data_uri()
        return render_template('reservoir.html', graph_data=graph_data)


@app.route('/verbruik')
def verbruik():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        verbruik = DbClass.getVerbruikTotaal(DbClass())
        return render_template('verbruik.html', verbruik=verbruik)


@app.errorhandler(404)
def pageNotFound(error):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('404.html',error=error)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='192.168.1.133')

