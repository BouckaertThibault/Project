from flask import Flask
from flask import flash, redirect, render_template, request, session, abort
import os
import pygal
from DbClass import DbClass
from pygal.style import Style

app = Flask(__name__)

TemperatuurStyle = Style(
  font_family='Lato',
  colors=('#f57e57','#f57e57')
)

ReservoirStyle = Style(
  font_family='Lato',
  colors=('#18AFD3','#18AFD3')
)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    Database = DbClass()
    value = DbClass.getPass(Database, request.form['username'])
    if request.form['password'] == value:
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
        graph = pygal.Line(style=TemperatuurStyle)
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
        graph = pygal.Line(style=ReservoirStyle)
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
        verbruik = round(float(DbClass.getVerbruikTotaal(DbClass())),2)
        return render_template('verbruik.html', verbruik=verbruik)


@app.errorhandler(404)
def pageNotFound(error):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('404.html',error=error)



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='169.254.10.1')